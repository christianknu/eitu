#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, sys, logging
import pytz, requests
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import ics_parser

URL_STUDY_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7Z6QQw0Z5gQ9f50on7Xx5YY00ZQ1ZYQycZw.ics'
URL_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6g7058yYQZXxQ5oQgZZ0vZ56Y1Q0f5c0nZQwYQ.ics'
URL_WIFI = 'https://www.itu.dk/people/bfri/eitu.json'
FAKES = [
    r'ScrollBar', # Locked
    r'Balcony', # Open space
    r'learnIT', # Virtual
    r'DesignLab', # Lab, locked
    r'InterMediaLab', # Lab, locked
    r'5A30',
    r'3A20', # Locked
    r'3A50', # Stuffed with computers
    r'3A52',
    r'^$', # Bug
]
ROOM_TO_WIFI = {
    'Aud 1': 'AUD1front0A11',
    'Aud 2': 'Aud2front0A35',
    'Aud 3': 'AUD32-3A56',
    'Aud 4': 'AUD44A60',
    '3A12/14': '3A12',
    '5A14-16': '5A14',
}

# Establish timezone
TZ = pytz.timezone('Europe/Copenhagen')

def format_date(date): return date.strftime('%a %b %d at %H:%M')

def format_wifi(reading):
    timestamp, clients = reading
    if clients > 5: return 'Many'
    if clients > 1: return 'Few'
    return 'Empty'

def clean_room(room):
    room = re.sub(r'^Room: ', '', room)
    room = re.sub(r' \(.*\)$', '', room)
    return room

def fake_room(room):
    return any([re.search(fake, room, re.IGNORECASE) for fake in FAKES])

def fetch_ics(url):
    logging.info('Fetching %s' % url)
    ics = requests.get(url).text
    logging.info('Parsing %s' % url)
    calendar = ics_parser.parse(ics)
    events = [{
        'rooms': map(clean_room, event['LOCATION'].split(', ')),
        'start': event['DTSTART'].astimezone(TZ),
        'end': event['DTEND'].astimezone(TZ),
        'uid': event['UID'],
    } for event in calendar]
    return events

def fetch_schedules():

    # Fetch iCalendar sources and parse events
    study_activities = fetch_ics(URL_STUDY_ACTIVITIES)
    activities = fetch_ics(URL_ACTIVITIES)
    events = study_activities + activities

    # Remove duplicate events
    events = {e['uid']: e for e in events}.values()

    # Establish schedules of events for each room
    logging.info('Establishing schedules')
    schedules = {}
    for event in events:
        for room in event['rooms']:
            if room not in schedules: schedules[room] = []
            schedules[room].append(event)
    schedules = {key: s for key, s in schedules.items() if not fake_room(key)}

    # Merge adjacent and overlapping events in each schedule
    logging.info('Merging events')
    for schedule in schedules.values():
        schedule.sort(key=lambda event: event['start'])
        merged = []
        for event in schedule:
            if merged and merged[-1]['end'] >= event['start']:
                merged[-1]['end'] = event['end']
            else:
                merged.append(event)
        schedule = merged

    return schedules

def fetch_wifi():
    return requests.get(URL_WIFI).json()

def render(schedules, wifi):

    # Establish present time
    NOW = datetime.now(TZ)

    # Determine the status of each room and how long it will be empty for
    logging.info('Determining status of rooms')
    rooms = []
    for name, schedule in schedules.items():
        wifi_name = ROOM_TO_WIFI[name] if name in ROOM_TO_WIFI else name
        room = {
            'name': name,
            'wifi': format_wifi(wifi[wifi_name]) if wifi_name in wifi else '?',
        }
        for event in schedule:
            if NOW <= event['start']:
                room['empty'] = True
                room['until'] = format_date(event['start'])
                room['empty_for'] = event['start'] - NOW
                break
            if event['start'] <= NOW <= event['end']:
                room['empty'] = False
                room['until'] = format_date(event['end'])
                room['empty_for'] = NOW - event['end']
                break
        if 'empty' not in room:
            room['empty'] = True
            room['for'] = '∞h ∞m'
        rooms.append(room)
    rooms.sort(key=lambda room: room['empty_for'], reverse=True)

    # Render index.html
    logging.info('Rendering index.html')
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('index.html')
    return template.render(
        title = 'EITU: Empty rooms at ITU',
        empty = [room for room in rooms if room['empty']],
        occupied = [room for room in rooms if not room['empty']],
        updated = format_date(NOW),
    )

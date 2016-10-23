#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, sys, logging
import requests
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
import eitu.ics_parser
import eitu.constants as constants
import eitu.formaters as formaters

def clean_room(room):
    room = re.sub(r'^Room: ', '', room)
    room = re.sub(r' \(.*\)$', '', room)
    return room

def fake_room(room):
    return any([re.search(fake, room, re.IGNORECASE) for fake in constants.FAKES])

def fetch_ics(url):
    logging.info('Fetching %s' % url)
    ics = requests.get(url).text
    logging.info('Parsing %s' % url)
    calendar = eitu.ics_parser.parse(ics)
    events = [{
                  'rooms': map(clean_room, event['LOCATION'].split(', ')),
                  'start': event['DTSTART'].astimezone(constants.TZ),
                  'end': event['DTEND'].astimezone(constants.TZ),
                  'uid': event['UID'],
              } for event in calendar]
    return events

def fetch_schedules():
    # Fetch iCalendar sources and parse events
    study_activities = fetch_ics(constants.URL_STUDY_ACTIVITIES)
    activities = fetch_ics(constants.URL_ACTIVITIES)
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
    try:
        return requests.get(constants.URL_WIFI).json()
    except:
        logging.error('Failed to fetch WiFi data')
        return {}



def render(schedules, wifi):
    # Establish present time
    NOW = datetime.now(constants.TZ)

    # Determine the status of each room and how long it will be empty for
    logging.info('Determining status of rooms')
    rooms = []
    for name, schedule in schedules.items():
        wifi_name = constants.ROOM_TO_WIFI[name] if name in constants.ROOM_TO_WIFI else name
        room = {
            'name': name,
            'wifi': formaters.format_wifi(wifi[wifi_name]) if wifi_name in wifi else '?',
        }
        for event in schedule:
            if NOW <= event['start']:
                room['empty'] = True
                room['until'] = formaters.format_date(event['start'])
                room['empty_for'] = event['start'] - NOW
                break
            if event['start'] <= NOW <= event['end']:
                room['empty'] = False
                room['until'] = formaters.format_date(event['end'])
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
    name = "Christian"
    template = env.get_template('index.html')
    return template.render(
        title='EITU: Empty rooms at ITU',
        empty=[room for room in rooms if room['empty']],
        occupied=[room for room in rooms if not room['empty']],
        updated=formaters.format_date(NOW),
        wifi=wifi,
    )

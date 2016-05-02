#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, logging
import pytz, requests
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import ics_parser

URL_STUDY_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7ZYQQZ0Z6gQ9Q1gfQvXx5fY90Zc0nY5yZo.ics'
URL_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6g706QyfQZXxQ5f5gon9vZ5YY0Q0Q1Z0QZcZY.ics'
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

# Logging
logging.getLogger().setLevel(logging.INFO)

# Fix unicode madness
reload(sys)
sys.setdefaultencoding('utf8')

# Establish timezone and present time
TZ = pytz.timezone('Europe/Copenhagen')
NOW = datetime.now(TZ)

def format_date(date): return date.strftime('%a %b %d at %H:%M')

def format_td(td): return '%02d hours' % (td.total_seconds() // 3600)

def format_wifi(reading):
    timestamp, clients = reading
    if clients > 5: return 'Many'
    if clients > 1: return 'Few'
    return 'Empty'

def clean_room(room):
    room = re.sub(r'^Room: ', '', room)
    room = re.sub(r' \(.*\)$', '', room)
    return room

def is_fake(room):
    return any([re.search(fake, room, re.IGNORECASE) for fake in FAKES])

def fetch_and_parse(url):
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

def eitu():

    # Fetch iCalendar sources and parse events
    study_activities = fetch_and_parse(URL_STUDY_ACTIVITIES)
    activities = fetch_and_parse(URL_ACTIVITIES)
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
    schedules = {key: s for key, s in schedules.items() if not is_fake(key)}

    # Merge adjacent and overlapping events in each schedule
    logging.info('Merging events')
    for schedule in schedules.itervalues():
        schedule.sort(key=lambda event: event['start'])
        merged = []
        for event in schedule:
            if merged and merged[-1]['end'] >= event['start']:
                merged[-1]['end'] = event['end']
            else:
                merged.append(event)
        schedule = merged

    # Load WiFi data
    wifi = requests.get(URL_WIFI).json()

    # Determine the status of each room and how long it will be empty for
    logging.info('Determining status of rooms')
    rooms = []
    for name, schedule in schedules.iteritems():
        wifi_name = ROOM_TO_WIFI[name] if name in ROOM_TO_WIFI else name
        room = {
            'name': name,
            'wifi': format_wifi(wifi[wifi_name]) if wifi_name in wifi else '?',
        }
        for event in schedule:
            if NOW <= event['start']:
                room['empty'] = True
                room['for'] = format_td(event['start'] - NOW)
                break
            if event['start'] <= NOW <= event['end']:
                room['empty'] = False
                room['for'] = format_td(event['end'] - NOW)
                break
        if 'empty' not in room:
            room['empty'] = True
            room['for'] = '∞h ∞m'
        rooms.append(room)
    rooms.sort(key=lambda room: room['for'], reverse=True)

    # Render index.html
    logging.info('Rendering index.html')
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    return template.render(
        title = 'EITU: Empty rooms at ITU',
        empty = [room for room in rooms if room['empty']],
        occupied = [room for room in rooms if not room['empty']],
        updated = format_date(NOW),
    )

def commit(html):
    github = {
        'url': 'https://api.github.com/repos/eitu/eitu.github.io/contents/index.html',
        'headers': {
            'Authorization': 'token %s' % os.environ['GITHUB_TOKEN'],
            'User-Agent': 'EITU',
        },
    }
    logging.info('Getting index.html from GitHub')
    file = requests.get(**github).json()
    github['json'] = {
        'path': 'index.html',
        'message': 'Updating index.html via GitHub API',
        'sha': file['sha'],
        'content': html.encode('utf-8').encode('base64', 'strict'),
        'committer': {
            'name': 'EITU',
            'email': 'eitu@itu.dk',
        },
    }
    logging.info('Updating index.html on GitHub')
    return requests.put(**github).json()

def handle(event, context):
    logging.info(commit(eitu()))
    return event

if __name__ == '__main__':
    with open('index.html', 'w+') as f: f.write(eitu())

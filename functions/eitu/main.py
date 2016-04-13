#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, logging
import pytz, requests
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import ics_parser

URL_STUDY_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7Z6QQw0Z5gQ9f50on7Xx5YY00ZQ1ZYQycZw.ics'
URL_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6g7058yYQZXxQ5oQgZZ0vZ56Y1Q0f5c0nZQwYQ.ics'
FAKES = [
    '0E01 ScrollBar', # Locked
    'Balcony_', # Open space
    'learnIT', # Virtual
    'DesignLab', # Lab, locked
    'InterMediaLab', # Lab, locked
    '5A30',
    '3A20', # Locked
    '3A50', # Stuffed with computers
    '3A52',
    '', # Bug
]

# Logging
logging.getLogger().setLevel(logging.INFO)

# Fix unicode madness
reload(sys)
sys.setdefaultencoding('utf8')

# Establish timezone and present time
TZ = pytz.timezone('Europe/Copenhagen')
NOW = datetime.now(TZ)

def format_date(date): return date.strftime('%a %b %d at %H:%M')

def clean_room(room):
    room = re.sub(r'^Room: ', '', room)
    room = re.sub(r' \(.*\)$', '', room)
    return room

def is_fake(room): return any([(room == fake) for fake in FAKES])

def fetch_and_parse(url):
    logging.info('Fetching %s' % url)
    ics = requests.get(url).text
    logging.info('Parsing %s' % url)
    calendar = ics_parser.parse(ics)
    events = [{
        'rooms': map(clean_room, event['LOCATION'].split(', ')),
        'start': event['DTSTART'].astimezone(TZ),
        'end': event['DTEND'].astimezone(TZ),
    } for event in calendar]
    return events

def eitu():

    # Fetch iCalendar sources and parse events
    study_activities = fetch_and_parse(URL_STUDY_ACTIVITIES)
    activities = fetch_and_parse(URL_ACTIVITIES)
    events = study_activities + activities

    # Establish schedules of events for each room
    logging.info('Establishing schedules')
    schedules = {}
    for event in events:
        for room in event['rooms']:
            if is_fake(room): continue
            if room not in schedules: schedules[room] = []
            schedules[room].append(event)

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

    # Determine the status of each room and how long it will be empty for
    logging.info('Determining status of rooms')
    rooms = []
    for name, schedule in schedules.iteritems():
        room = {'name': name}
        for event in schedule:
            if NOW <= event['start']:
                room['empty'] = True
                room['until'] = format_date(event['start'])
                room['empty_for'] = event['start'] - NOW
                break
            if event['start'] <= NOW <= event['end']:
                room['empty'] = False
                room['until'] = format_date(event['end'])
                room['empty_for'] = timedelta.min
                break
        if 'empty' not in room:
            room['empty'] = True
            room['until'] = 'For the foreseeable future'
            room['empty_for'] = timedelta.max
        rooms.append(room)
    rooms.sort(key=lambda room: room['empty_for'], reverse=True)

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

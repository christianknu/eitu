#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
import pytz, requests
from icalendar import Calendar
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

URL = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7ZYQQZ0Z5gQ9Q1gfQvXx5fY70Zc0nY5yZo.ics'
FAKE = {'learnIT': True, 'Balcony_': True}

def format_date(date): return date.strftime('%a %b %d at %H:%M')

def clean_room(room):
    room = re.sub(r'^Room: ', '', room)
    room = re.sub(r' \(.*\)$', '', room)
    return room

def eitu():

    # Establish timezone and present time
    tz = pytz.timezone('Europe/Copenhagen')
    now = datetime.now(tz)

    # Fetch iCalendar source and parse events
    iCalendar = requests.get(URL).text
    calendar = Calendar.from_ical(iCalendar)
    events = [{
        'rooms': map(clean_room, str(c['LOCATION']).split(', ')),
        'start': c['DTSTART'].dt.astimezone(tz),
        'end': c['DTEND'].dt.astimezone(tz),
    } for c in calendar.walk('vevent')]

    # Establish schedules of events for each room
    schedules = {}
    for event in events:
        for room in event['rooms']:
            if room in FAKE: continue
            if room not in schedules: schedules[room] = []
            schedules[room].append(event)

    # Merge adjacent and overlapping events in each schedule
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
    rooms = []
    for name, schedule in schedules.iteritems():
        room = {
            'name': room,
            'status': None,
            'empty_for': None,
        }
        for event in schedule:
            if now <= event['start']:
                room['status'] = '🎉 Empty until %s' % format_date(event['start'])
                room['empty_for'] = event['start'] - now
                break
            if event['start'] <= now <= event['end']:
                room['status'] = '👾 Occupied until %s' % format_date(event['end'])
                room['empty_for'] = timedelta.min
                break
        if room['status'] == None:
            room['status'] = '🎉 Empty for the foreseeable future'
            room['empty_for'] = timedelta.max
        rooms.append(room)
    rooms.sort(key=lambda room: room['empty_for'], reverse=True)

    # Render index.html
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    content = template.render(
        title = 'EITU: Empty rooms at ITU',
        rooms = rooms,
        updated = format_date(now),
    ).encode('utf-8')

    # Commit index.html to GitHub
    github = {
        'url': 'https://api.github.com/repos/eitu/eitu.github.io/contents/index.html',
        'headers': {
            'Authorization': 'token %s' % os.environ['GITHUB_TOKEN'],
            'User-Agent': 'EITU',
        },
    }
    file = requests.get(**github).json()
    github['json'] = {
        'path': 'index.html',
        'message': 'Updating index.html via GitHub API',
        'sha': file['sha'],
        'content': content.encode('base64', 'strict'),
        'committer': {
            'name': 'EITU',
            'email': 'eitu@itu.dk',
        },
    }
    print requests.put(**github).json()

def handle(event, context):
    eitu()
    return event

if __name__ == '__main__':
    handle({}, None)

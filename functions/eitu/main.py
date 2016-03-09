#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytz
import requests
from icalendar import Calendar
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

URL = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7ZYQQZ0Z5gQ9Q1gfQvXx5fY70Zc0nY5yZo.ics'
BOXES = ['2A03', '2A07', '3A03', '4A01', '4A03', '4A07', '5A03', '5A07']
FAKE = {'learnIT': True, 'Balcony_': True}
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

def eitu():
    local_tz = pytz.timezone('Europe/Copenhagen')
    now = datetime.now(local_tz)

    ics = requests.get(URL).text
    gcal = Calendar.from_ical(ics)

    events = [{
        'rooms': str(c['LOCATION']).replace('Room: ', '').split(', '),
        'start': c['DTSTART'].dt.astimezone(local_tz),
        'end': c['DTEND'].dt.astimezone(local_tz),
    } for c in gcal.walk('vevent')]

    schedules = {}
    for event in events:
        for room in event['rooms']:
            if room in FAKE: continue
            if room not in schedules:
                schedules[room] = []
            schedules[room].append(event)

    rooms = []
    for room, schedule in schedules.iteritems():
        schedule.sort(key=lambda event: event['start'])
        status = None
        empty_for = None
        for event in schedule:
            if now <= event['start']:
                status = 'Empty until %s' % event['start'].strftime('%c')
                empty_for = event['start'] - now
                break
            if event['start'] <= now <= event['end']:
                status = 'Occupied until %s' % event['end'].strftime('%c')
                empty_for = timedelta.min
                break
        if status == None:
            status = 'Empty'
            empty_for = timedelta.max
        rooms.append({
            'name': room,
            'status': status,
            'empty_for': empty_for,
        })
    rooms.sort(key=lambda room: room['empty_for'], reverse=True)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    content = template.render(
        title = 'EITU: Empty rooms at ITU',
        boxes = BOXES,
        rooms = rooms,
        updated = now.strftime('%c'),
    ).encode('utf-8')

    github = {
        'url': 'https://api.github.com/repos/eitu/eitu.github.io/contents/index.html',
        'headers': {
            'Authorization': 'token %s' % GITHUB_TOKEN,
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

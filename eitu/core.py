#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import time
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

import eitu.constants as constants
import eitu.formaters as formaters
import eitu.time_edit as timeEdit
from eitu.wifi import retrieve, write_database, read_database, stale_database


def fake_room(room):
    return any([re.search(fake, room, re.IGNORECASE) for fake in constants.FAKES])


def fetch_schedules():
    logging.info('writing database')
    if timeEdit.stale_database(time.time()):
        timeEdit.write_database()

    logging.info('Reading database')
    events = timeEdit.get_events()

    # Remove duplicate events
    events = {e['uid']: e for e in events}.values()

    # Establish schedules of events for each room
    logging.info('Establishing schedules')
    schedules = {}
    for event in events:
        for room in event['location']:
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
        if(stale_database(time.time())):
            data = retrieve()
            write_database(data)
            # could be cleaned up so that retieved data is converted to correct format without
            # writing to database and then reading it
            occupancy_rooms = read_database()
        else:
            occupancy_rooms = read_database()
        return occupancy_rooms
    except:
        logging.error('Failed to fetch WiFi data')
        return {}


def render():
    # Establish present time
    NOW = datetime.now(constants.TZ)

    # Determine the status of each room and how long it will be empty for
    logging.info('Determining status of rooms')

    # Render index.html
    logging.info('Rendering index.html')
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('index.html')
    return template.render(
        updated=formaters.format_date(NOW),
    )

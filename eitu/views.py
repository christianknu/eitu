from django.http import HttpResponse, JsonResponse
import logging
from eitu.core import fetch_schedules, render, fetch_wifi

import eitu.constants as constants
import eitu.formaters as formaters
from datetime import datetime
import pytz

import json


def index(request):
    # Logging
    logging.getLogger().setLevel(logging.INFO)

    schedules = fetch_schedules()
    wifi = fetch_wifi()
    html = render(schedules, wifi)

    return HttpResponse(html)


def getRooms(request):
    NOW = datetime.now(constants.TZ)
    schedules = fetch_schedules()
    wifi = fetch_wifi()

    logging.info('Determining status of rooms')
    rooms = []
    for name, schedule in schedules.items():
        wifi_name = constants.ROOM_TO_WIFI[name] if name in constants.ROOM_TO_WIFI else name
        room = {
            'name': name,
            'wifi': formaters.format_wifi(wifi[wifi_name]) if wifi_name in wifi else 'No WiFi Data',
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

    for name in constants.FREE_ROOMS_WITH_WIFI:
        wifi_name = constants.FREE_ROOMS_WITH_WIFI[name] if name in constants.FREE_ROOMS_WITH_WIFI else name
        emptyroom = {
        'name': name,
        'wifi': formaters.format_wifi(wifi[wifi_name]) if wifi_name in wifi else 'No WiFi Data',
        }
        emptyroom['empty'] = True
        emptyroom['until'] = NOW - NOW
        emptyroom['empty_for'] = NOW- NOW
        rooms.append(emptyroom)

    rooms.sort(key=lambda room: room['empty_for'], reverse=True)

    empty=[dict([("room", room["name"]), ("wifi", room["wifi"]), ("until", str(room["until"]))]) for room in rooms if room['empty']]
    booked=[dict([("room", room["name"]), ('empty', room['empty']), ("wifi", room["wifi"]), ("until", str(room["until"]))]) for room in rooms if not room['empty']]

    return JsonResponse({ "empty":empty, "booked":booked })
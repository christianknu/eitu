import csv, re
from datetime import datetime
import requests
import ics_parser
import pytz

URL_STUDY_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7Z6QQw0Z5gQ9f50on7Xx5YY00ZQ1ZYQycZw.ics'
URL_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6g7058yYQZXxQ5oQgZZ0vZ56Y1Q0f5c0nZQwYQ.ics'
TZ = pytz.timezone('Europe/Copenhagen')

def fetch_and_parse(url):
    return ics_parser.parse(requests.get(url).text)

def write(things, path):
    with open(path, 'w') as csvfile:
        fieldnames = set()
        for t in things: fieldnames = fieldnames | set(t.keys())
        writer = csv.DictWriter(csvfile, fieldnames=list(fieldnames))
        writer.writeheader()
        for t in things:
            for key, value in t.items():
                if isinstance(value, datetime):
                    t[key] = value.astimezone(TZ).isoformat()
            writer.writerow(t)

# Fetch and parse iCalendar events
study_activities = fetch_and_parse(URL_STUDY_ACTIVITIES)
activities = fetch_and_parse(URL_ACTIVITIES)
events = study_activities + activities

# Remove duplicates and sort
events = {e['UID']: e for e in events}.values()
events = sorted(events, key=lambda e: e['DTSTART'])

# Generate bookings
bookings = []
for e in events:
    for room in e['LOCATION'].split(', '):
        bookings.append({
            'room': re.sub(r'^Room: ', '', room),
            'start': e['DTSTART'],
            'end': e['DTEND'],
        })

# Write CSV files
print(len(events))
write(events, 'events.csv')
print(len(bookings))
write(bookings, 'bookings.csv')

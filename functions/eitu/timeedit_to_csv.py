import requests
import csv
import ics_parser

URL_STUDY_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7Z6QQw0Z5gQ9f50on7Xx5YY00ZQ1ZYQycZw.ics'
URL_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6g7058yYQZXxQ5oQgZZ0vZ56Y1Q0f5c0nZQwYQ.ics'

def fetch_and_parse(url):
    return ics_parser.parse(requests.get(url).text)

# Fetch and parse iCalendar events
study_activities = fetch_and_parse(URL_STUDY_ACTIVITIES)
activities = fetch_and_parse(URL_ACTIVITIES)
events = study_activities + activities

# Remove duplicate events
events = {e['UID']: e for e in events}.values()

# Write csv
with open('timeedit.csv', 'w') as csvfile:
    fieldnames = set()
    for e in events: fieldnames = fieldnames | set(e.keys())
    writer = csv.DictWriter(csvfile, fieldnames=sorted(list(fieldnames)))
    writer.writeheader()
    for e in events: writer.writerow(e)

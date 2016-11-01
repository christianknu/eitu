import os, re, logging, requests
from eitu.models import TimeEditEvent
import eitu.constants as constants
import eitu.ics_parser as parser

glob_time_edit_last_write = 0
TIME_EDIT_FREQ_FETCH = 21600  # every 60 seconds


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
    return parser.parse(ics)


def write_database():
    # Fetch iCalendar sources and parse events
    study_activities = fetch_ics(constants.URL_STUDY_ACTIVITIES)
    activities = fetch_ics(constants.URL_ACTIVITIES)
    events = study_activities + activities

    TimeEditEvent.objects.all().delete()
    for event in events:
        o = TimeEditEvent(
            uid=event['UID'],
            datetime_start=event['DTSTART'].astimezone(constants.TZ),
            datetime_end=event['DTEND'].astimezone(constants.TZ),
            datetime_stamp=event['DTSTAMP'].astimezone(constants.TZ),
            datetime_lastModified=event['LAST-MODIFIED'].astimezone(constants.TZ),
            summary=event['SUMMARY'],
            location=event['LOCATION'],
            description=event['DESCRIPTION'])
        o.save()


def clean_room(room):
    room = re.sub(r'^Room: ', '', room)
    room = re.sub(r' \(.*\)$', '', room)
    return room


def get_events():
    calendar = TimeEditEvent.objects.all()
    events = []
    for event in calendar:
        obj = {
            'uid': event.uid,
            'start': event.datetime_start.astimezone(constants.TZ),
            'end': event.datetime_end.astimezone(constants.TZ),
            'timeStamp': event.datetime_stamp.astimezone(constants.TZ),
            'lastModified': event.datetime_lastModified.astimezone(constants.TZ),
            'summary': event.summary,
            'location': map(clean_room, event.location.split(', ')),
            'description': event.description
        }
        events.append(obj)
    events = {e['uid']: e for e in events}.values()
    return events


def stale_database(time_now):
    time_dif = time_now - glob_time_edit_last_write

    if (time_dif > TIME_EDIT_FREQ_FETCH):
        return True
    else:
        return False

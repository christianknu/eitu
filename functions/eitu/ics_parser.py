from datetime import datetime
import pytz

def lines_to_event(lines):
    # Unescape double escapes
    lines = [line.replace('\\', '') for line in lines]
    # Transform lines to event
    event = {}
    key = None
    for line in lines:
        if not line.startswith(' '):
            key, value = line.split(':', 1)
            event[key] = value
        elif key is not None:
            event[key] += line[1:]
    # Convert values to datetimes where possible
    # Example datetime: 20160324T164512Z
    for key, value in event.items():
        try:
            event[key] = datetime.strptime(value, '%Y%m%dT%H%M%SZ').replace(tzinfo=pytz.UTC)
        except:
            pass
    return event

def parse(ical):
    # Unicode utf-8
    ical = unicode(ical).encode('utf-8')
    # Normalize linebreaks and split ical into list of lines
    ical = ical.replace('\r\n', '\n')
    iterator = iter(ical.split('\n'))
    # Break lines up into a list of events
    events = []
    while True:
        try:
            line = iterator.next()
            if 'BEGIN:VEVENT' == line:
                line = iterator.next()
                lines = []
                while not 'END:VEVENT' == line:
                    lines.append(line)
                    line = iterator.next()
                events.append(lines_to_event(lines))
        except StopIteration:
            return events

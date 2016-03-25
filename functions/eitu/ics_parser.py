from datetime import datetime
import pytz

def lines_to_event(lines):
    event = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            value = value.replace('\\', '')
            try:
                # Example datetime 20160324T164512Z
                value = datetime.strptime(value, '%Y%m%dT%H%M%SZ').replace(tzinfo=pytz.UTC)
            except:
                pass
            event[key] = value
    return event

def parse(ical):
    iterator = iter(ical.split('\r\n'))
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

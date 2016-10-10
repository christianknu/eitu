
def format_date(date): return date.strftime('%a %b %d at %H:%M')


def format_wifi(reading):
    timestamp, clients = reading
    if clients > 5:
        return 'Many'
    if clients > 1:
        return 'Few'
    return 'Empty'
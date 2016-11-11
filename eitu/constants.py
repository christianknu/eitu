import pytz

URL_STUDY_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6Q7Z6QQw0Z5gQ9f50on7Xx5YY00ZQ1ZYQycZw.ics'
URL_ACTIVITIES = 'https://dk.timeedit.net/web/itu/db1/public/ri6g7058yYQZXxQ5oQgZZ0vZ56Y1Q0f5c0nZQwYQ.ics'
URL_WIFI = 'https://www.itu.dk/people/bfri/eitu.json'
FAKES = [
    r'ScrollBar',  # Locked
    r'Balcony',  # Open space
    r'learnIT',  # Virtual
    r'DesignLab',  # Lab, locked
    r'InterMediaLab',  # Lab, locked
    r'5A30',
    r'3A20',  # Locked
    r'3A50',  # Stuffed with computers
    r'3A52',
    r'Student work spaces',
    r'Meeting room',
    r'^$',  # Bug
]
ROOM_TO_WIFI = {
    'Aud 1': 'AUD1front0A11',
    'Aud 2': 'Aud2front0A35',
    'Aud 3': 'AUD32-3A56',
    'Aud 4': 'AUD44A60',
    '3A12/14': '3A12',
    '5A14-16': '5A14',
    '2A12-14': '2A12',
    '4A14-16': '4A14',
}

FREE_ROOMS_WITH_WIFI = {
    '4A62(Corner)':'4A62',
    '2A40(Corner)':'2A40',
    '3A58(Corner)':'3A58',
    '4A32(Corner)':'4A32',
    '5A32(Corner)':'5A32',
    '5A44(Corner)':'5A44',
    '5A54(Corner)':'5A54',
    '5A62(Corner)':'5A62',
    '2A03(Glass)':'2A03',
    '2A07(Glass)':'2A07',
    '3A03(Glass)':'3A03',
    '4A01(Glass)':'4A01',
    '4A03(Glass)':'4A03',
    '4A07(Glass)':'4A07',
    '5A03(Glass)':'5A03',
    '5A07(Glass)':'5A07',
}
# Establish timezone
TZ = pytz.timezone('Europe/Copenhagen')

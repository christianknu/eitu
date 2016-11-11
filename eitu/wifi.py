import time
import requests
from django.db import transaction
from eitu.models import wifi_occupancy

glob_last_write = 0
FREQ_FETCH = 60  # every 60 seconds


def retrieve():
    response = requests.get('http://training.itu.dk:8080/api/occupancy/')
    data = response.json()
    return data


def occupancy(data):
    occupancy_rooms = {}
    for obj in data:
        room = obj["location"]["name"]
        numberOfClients = obj["numberOfClient"]
        timestamp = obj["timestamp"]
        occupancy_rooms[room] = (timestamp, numberOfClients)
    return occupancy_rooms


def empty_rooms(occupancy_rooms):
    empty = []
    for key, value in occupancy_rooms.items():
        if (value == 0):
            empty.append(key)
    return empty


@transaction.atomic
def write_database(data):
    global glob_last_write
    glob_last_write = time.time()

    wifi_occupancy.objects.all().delete()
    for obj in data:
        o = wifi_occupancy(room_name=obj["location"]["name"], room_occupancy=obj["numberOfClient"],
                           timestamp=obj["timestamp"])
        o.save()


def read_database():
    occupancy_rooms = {}
    all_entries = wifi_occupancy.objects.all()
    for obj in all_entries:
        room = obj.room_name
        numberOfClients = obj.room_occupancy
        timestamp = obj.timestamp
        occupancy_rooms[room] = (timestamp, numberOfClients)
    return occupancy_rooms


def stale_database(time_now):
    timedif = time_now - glob_last_write

    if (timedif > FREQ_FETCH):
        return True
    else:
        return False

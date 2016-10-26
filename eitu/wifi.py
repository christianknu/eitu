import json
import requests
from eitu.models import Occupancy

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
		occupancy_rooms[room] = (timestamp,numberOfClients)
	return occupancy_rooms

def empty_rooms(occupancy_rooms):
	empty = []
	for key,value in occupancy_rooms.items():
		if(value == 0):
			empty.append(key)
	return empty

def write_database(data):
	for obj in data:
		o = Occupancy(room_name = obj["location"]["name"], room_occupancy = obj["numberOfClient"], timestamp= obj["timestamp"])
		o.save()

def read_database():
	occupancy_rooms = {}
	all_entries = Occupancy.objects.all()
	for obj in all_entries:
		room = obj.room_name
		numberOfClients = obj.room_occupancy
		timestamp = obj.timestamp
		occupancy_rooms[room] = (timestamp,numberOfClients)
	return occupancy_rooms
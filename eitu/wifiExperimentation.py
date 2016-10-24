import json
import requests
from pprint import pprint

def retrieve():
	response = requests.get('http://training.itu.dk:8080/api/occupancy/')
	data = response.json()
	return data

def occupancy(data):
	occupancy_rooms = {}
	for obj in data:
		room = obj["location"]["room"]
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

def write_to_file(occupancy_rooms):
	with open('occupancy.json', 'w') as outfile:
		json.dump(occupancy_rooms, outfile)

data = retrieve()
rooms = occupancy(data)

write_to_file(rooms)
pprint(rooms)

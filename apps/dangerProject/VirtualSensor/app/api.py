from app import app
from app.bulletin import Bulletin
from app.virtualSensorCore import VirtualSensorCore
from flask import request, jsonify

@app.route('/api/notify_run', methods = ['POST'])
def notify_run():
	content = request.json
	print "Ricevuto: " + str(content)

	user = content['user']
	state = content['state']
	building = content['building']
	room = content['room']

	print "User: " + user + " is " + state + " !"
	print "Building: " + building
	print "Room: " + room

	bulletin = Bulletin(user, state, building, room)

#	app.virtual_sensor_core.handle_new_bulletin(bulletin)

	return "WARNING Sent"

@app.route('/api/notify_run', methods = ['GET'])
def returnSuca():
	return "SUCA"



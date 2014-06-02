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
	building = content['buildings']
	room = content['room']

	print "User: " + user + " is " + state + " !"
	print "Building: " + building
	print "Room: " + room

	bulletin = Bulletin(user, state, building, room)

	app.virtual_sensor_core.handle_new_bulletin(bulletin)

	return "WARNING Sent"

@app.route('/api/notify_run', methods = ['GET'])
def returnSuca():
	return "SUCA"


@app.route('/api/check_sensor_status', methods = ['GET'])
def check_sensor_status():
	"""Called from the GORILLA_ATTACK_DRIVER (temporary name) from building
	rules"""

	message = {'status' : 'False'}

	trigger_run = app.virtual_sensor_core.trigger_run

	if trigger_run is not None:
		message['status'] = 'True'
		message['building'] = trigger_run['building']
		message['room'] = trigger_run['room']

	return jsonify(message)




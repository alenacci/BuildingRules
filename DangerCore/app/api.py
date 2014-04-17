from app import app
from flask import request, jsonify
from app.commons.bulletin import *
from app.core.dangerCore import DangerCore

@app.route('/api/send_bulletin', methods = ['POST'])
def decodeBulletin():
	content = request.json
	print "Ricevuto: " + str(content)

	danger_type = content['danger_type']
	building = content['building']
	room = content['room']

	print "Danger Type: " + danger_type
	print "Building: " + building
	print "Room: " + room

	bulletin = Bulletin(danger_type, building, room)

	app.danger_core.handle_new_bulletin(bulletin)


	return "Bullettin Sent"



@app.route('/api/check_trigger_status', methods = ['POST'])
def checkTriggerStatus():
	content = request.json

	trigger = content['trigger_name']
	building = content['building']
	room = content['room']

	bulletin = Bulletin(trigger, building, room)

	response = app.danger_core.is_active(bulletin)

	print "Trigger_status = " + str(response)
    
	return jsonify(trigger_status = str(response))

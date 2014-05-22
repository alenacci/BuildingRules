from app import app
from flask import request, jsonify
from app.commons.bulletin import *
from tools.triggerRequestHelper import *
from app.core.dangerCore import DangerCore
from tools.log import *



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

	response = app.danger_core.is_active(bulletin) and app.danger_core.TEST_confirmed_from_building_manager

	print "Trigger_status = " + str(response)

	return jsonify(trigger_status = str(response) )


#This method returns a json containing all the information about the current
#situation of danger.
#It is used by the building manager to check whether there are pending
#situations of danger
@app.route('/api/get_current_status', methods = ['GET'])
def getCurrentStatus():
	#Three level of 'status' are available:
	#OK		Everything fine
	#ALERT	There are situations that be double checked, it may be a situation of danger
	#DANGER	A situation of danger is happening

	message = {}

	#TODO This is just a dummy implementation
	if len(app.danger_core.bulletin_list) > 0:
		b = app.danger_core.bulletin_list[0]
		message['building'] = b.building
		message['room'] = b.room
		message['description'] = 'Unusual movements, smoke detected'
		message['status'] = 'ALERT'
	else:
		message['status'] = 'OK'

	return jsonify(message)

#This method is used by the building manager client in order
#to confirm or dismiss a pending danger
@app.route('/api/building_manager/confirm_danger', methods = ['POST'])
def confirmDanger():
	content = request.json
	confirmed = content['confirmed']

	if confirmed == 'True':
		print "Danger Confirmed"
		#TODO come indichiamo che il pericolo e' confermato?
		app.danger_core.TEST_confirmed_from_building_manager = True
		request_rules_real_time_update_async()

	return jsonify(received = 'true')


#This method is used by the user client in order
#to retrieve the pending notifications
#The POST json contains the timestamp of the last
#notification received.
#The response is a json with all the notification since then
@app.route('/api/user/get_notifications', methods = ['POST'])
def getNotification():
	content = request.json
	timestamp = content['timestamp']

	###FOR TESTING
	log_event(None)

	response = {}

	if app.danger_core.TEST_confirmed_from_building_manager == True:
		response['new_notifications'] = 'True'
		#TODO FILL THE NOTIFICATIONS!!
	else:
		response['new_notifications'] = 'False'

	return jsonify(response)



from app import app
from flask import request, jsonify
from app.commons import *
from app.commons.notification import Notification
from app.commons.bulletin import Bulletin
from app.commons.user import User
from app.core import connectionAnalyzer
from tools.triggerRequestHelper import *
from app.core.dangerCore import DangerCore
from tools.log import *
import os
from flask import send_file


@app.route('/api/send_bulletin', methods = ['POST'])
def decodeBulletin():
	content = request.json
	print "Ricevuto: " + str(content)

	danger_type = content['danger_type']
	building = content['buildings']
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
	building = content['buildings']
	room = content['room']

	bulletin = Bulletin(trigger, building, room)

	response = app.danger_core.is_active(bulletin) and app.danger_core.TEST_confirmed_from_building_manager

	print "Trigger_status = " + str(response)

	return jsonify(trigger_status = str(response) )


#This method returns a json containing all the information about the current
#situation of danger.
#It is used by the buildings manager to check whether there are pending
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

#This method is used by the buildings manager client in order
#to confirm or dismiss a pending danger
@app.route('/api/building_manager/confirm_danger', methods = ['POST'])
def confirmDanger():
	content = request.json
	confirmed = content['confirmed']

	if confirmed == 'True':
		print "Danger Confirmed"
		#TODO come indichiamo che il pericolo e' confermato?
		app.danger_core.TEST_confirmed_from_building_manager = True

		nMgr = app.danger_core.notificationsManager
		notification = Notification("danger")
		nMgr.addNotification(notification)

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
	timestamp = int(content['timestamp'])


	#user_id = content['user_id']
	user_id = "Andre"

	connectionAnalyzer = app.danger_core.connection_analyzer
	connectionAnalyzer.lock.acquire()
	connectionAnalyzer.update_user_in_list(user_id)
	connectionAnalyzer.lock.release()

	###FOR TESTING
	log_event(None)

	response = {}

	nMgr = app.danger_core.notificationsManager
	notifications = nMgr.getNotificationsFromTime(timestamp)

	#if timestamp is 0, we make a "empty" notification
	#just to let the application set to the current timestamp
	if(timestamp == 0):
		response['new_notifications'] = 'True'
		n = Notification("empty")
		n.timestamp = nMgr.timeCount
		response['notifications'] = [n.__dict__]
	elif( len(notifications) > 0):
		n_list = []
		for n in notifications:
			n_list.append(n.__dict__)
			print(n.__dict__)
		response['new_notifications'] = 'True'
		response['notifications'] = n_list
	else:
		response['new_notifications'] = 'False'



	#if app.danger_core.TEST_confirmed_from_building_manager == True:
	#	response['new_notifications'] = 'True'
		#TODO FILL THE NOTIFICATIONS!!
	#else:
	#	response['new_notifications'] = 'False'

	return jsonify(response)


#This method request ALL the devices to record and send
#an audio sample. To be modified
@app.route('/api/request_audio_sensing', methods = ['GET'])
def requestAudioSensing():
	#TODO specify which device has to receive this notification
	nMgr = app.danger_core.notificationsManager
	notification = Notification("action-record_audio")
	nMgr.addNotification(notification)

	response = {}
	response['status'] = 'OK'

	return jsonify(response)

#Download the audio file
@app.route("/api/download_audio_sensing")
def downloadAudioSensing():

	aMgr = app.danger_core.audioRecordsManager
	filepath = aMgr.get_file()

	if filepath is not None:
		return send_file(filepath)
	else:
		#give a "no content"
		return '', 204


#Download the audio file
@app.route("/audioUploads/<filename>")
def download2():

	aMgr = app.danger_core.audioRecordsManager
	filepath = aMgr.get_file()
	if file is not None:
		print "file " + filepath
		return app.send_static_file(filepath)
	else:
		#give a "no content"
		return '', 204

#This method is used for upload an audio file
#of the environment
@app.route('/api/user/upload_audio', methods = ['POST'])
def uploadAudio():
	audioMgr = app.danger_core.audioRecordsManager

	#print(str(len(request.files)))
	file = request.files['file']
	print(file)
	if file: #and allowed_file(file.filename):
		filename = audioMgr.get_new_filename(file.filename)
		file.save(os.path.join(audioMgr.AUDIO_DIR, filename))

	message = {}
	message['status'] = 'OK'

	return jsonify(message)


@app.route('/api/register_user', methods = ['POST'])
def registerUser():
	content = request.json
	print "Ricevuto: " + str(content)

	id = content['id']
	room = content['room']

	print "ID: " + str(id)
	print "Room: " + str(room)

	# TODO fix constructor
	user = User(id, room=room)

	app.danger_core.register_user(user)

	return jsonify( { 'status': "ok" } )

@app.route('/api/get_users', methods = ['POST'])
def getUsers():
	content = request.json
	print "Ricevuto: " + str(content)

	room = content['room']

	users_count = len(app.danger_core.get_users_by_room(room))

	return jsonify( { 'users': users_count } )


@app.route('/api/get_all', methods = ['GET'])
def getAllUsers():

	users = app.danger_core.get_users_by_room("*")
	users_json = []

	for u in users:
		user = {
			'id': u.user_id,
			'room': u.room
		}
		users_json.append(user)


	return jsonify( { 'users': users_json } )

from app import app
from flask import request

@app.route('/api/send_bulletin', methods = ['POST'])
def decodeBulletin():
	content = request.json
	print "Ricevuto: " + str(content)

	print "Building: " + content['building']
	print "Room: " + content['room']
	print "Danger Type: " + content['danger_type']

	return "Update requested"

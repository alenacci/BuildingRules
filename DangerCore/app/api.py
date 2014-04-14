from app import app
from flask import request

from app.commons.bulletin import *

@app.route('/api/send_bulletin', methods = ['POST'])
def decodeBulletin():
	content = request.json
	print "Ricevuto: " + str(content)

	print "Building: " + content['building']
	print "Room: " + content['room']
	print "Danger Type: " + content['danger_type']

	bulletin = Bulletin()
	bulletin.danger_type = "bau"

	app.danger_core.handle_new_bulletin(bulletin)


	return "Update requested"

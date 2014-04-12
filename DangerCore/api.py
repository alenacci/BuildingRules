@api.route('/api/send_bulletin', methods = ['POST'])
def decodeBulletin():
	content = request.json()
    print "Ricevuto: " + content

    content = json.load(content)
    print "Tradotto in: " + content

    print "Building: " + content['building']
    print "Room: " + content['room']
    print "Danger Type: " + content['danger_type']

	return "Update requested"

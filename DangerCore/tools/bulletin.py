import urllib2,json

# prepare and send a bulletin via Danger's API with the information provided
def send_bulletin(building,room,danger_type):
	data = {
			'building': building,
			'room' : room,
			'danger_type' : danger_type
	}

	req = urllib2.Request('http://localhost:2001/api/send_bulletin')
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(data))
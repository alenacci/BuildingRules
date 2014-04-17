import urllib2,json

# prepare and send a bulletin via Danger's API with the information provided
def check_trigger_status(trigger_name,building,room):
	data = {
			'trigger_name' : trigger_name,
			'building': building,
			'room' : room
	}

	req = urllib2.Request('http://localhost:2001/api/check_trigger_status')
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(data))


	status = json.load((response)['trigger_status'])

	return status

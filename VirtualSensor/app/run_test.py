import urllib2,json

data = {
			'user' : "andrea",
			'state' : "running",
			'building': "DEI",
			'room' : "28"
}

req = urllib2.Request('http://localhost:2560/api/notify_run')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
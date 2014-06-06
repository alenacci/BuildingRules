import urllib2,json,threading

# prepare and send a bulletin via Danger's API with the information provided
def check_sensor_status():

	response = urllib2.urlopen('http://localhost:2560/api/check_sensor_status')

	status = json.load(response)

	return status

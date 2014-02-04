import sys
import json
import random
import string
import datetime
import time
import signal
import os.path
import httplib2
import urllib
import os

#ob-ucsd-cse.ucsd.edu:8000/dataservice/
#sensor_type = 'Zone Temperature'
#zone = 'RM-B200B'
#BD api key: 7d0a9b2f-11bd-40da-8ff5-f7836fe468c3
#auth_token: 1

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class RoomTriggerDriver(GenericTriggerDriver):


	# parameters = {}

	# parameters["operation"] = "AFTER"
	# parameters["val_0"] = 

	def __init__(self, parameters):
		self.parameters = parameters
		self.api_key = '7d0a9b2f-11bd-40da-8ff5-f7836fe468c3';
		self.auth_token = '1';
		self.http = httplib2.Http()

	
	def eventTriggered(self):

		import random

		if self.parameters["operation"] == "CHECK_PRESENCE":
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))


		elif self.parameters["operation"] == "CHECK_ABSENCE":
			
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TEMPERATURE_IN_RANGE":

			#print self.parameters["buildingName"]
			#print self.parameters["roomName"]
			#print self.parameters["groupId"]

			sensor_uuid = self.get_uuid_from_context('Zone Temperature', 'B200B')
			temperature = self.read_present_value_by_uuid(sensor_uuid)

			
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))

		
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __str__(self):
		return "RoomTriggerDriver: "


	def get_uuid_from_context(self, sensor_type, zone):
	    try:
	        response = self.http.request(
	        "http://ob-ucsd-cse.ucsd.edu:8000/dataservice/api/sensors/context/Type=" + sensor_type + "+Room=Rm-" + zone,
	        "GET",
	        headers={'content-type':'application/json', 'X-BD-Api-Key': self.api_key, 'X-BD-Auth-Token': self.auth_token}
	        )
	        #print "response: ", response

	    except Exception as e:
	        raise BuildingDepotError('Could not search by given context! ' + str(e))

	    response = response[1]
	    response_json = json.loads(response) 
	    sensors_list = response_json["sensors"]

	    try:
	        uuid = sensors_list[0]["uuid"]
	    except Exception as e: 
	        raise BuildingDepotError('Could not extract uuid out of response! ' + str(e))
	    
	    #print "Sensor uuid is " + uuid
	    
	    return uuid

	def read_present_value_by_uuid(self, sensor_uuid, sensorpoint_name = "PresentValue"):
	    url = "http://ob-ucsd-cse.ucsd.edu:8000/dataservice/api/sensors/" + sensor_uuid + "/sensorpoints/" + sensorpoint_name + "/datapoints"

	    try:
	        response = self.http.request(
	        url,
	        "GET",
	        headers={"X-BD-Api-Key": self.api_key, "X-BD-Auth-Token": self.auth_token}
	        )
	        #print response
	        response_json = json.loads(response[1])
	        datapoints = response_json["datapoints"]
	        for time, data in datapoints[0].iteritems():
	            value = float(data)
	    except Exception as e:
	    	raise BuildingDepotError('Error, could not read present value! ' + str(e))

	    return value		
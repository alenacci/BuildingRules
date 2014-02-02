import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class WeatherTriggerDriver(GenericTriggerDriver):


	# parameters = {}

	# parameters["operation"] = "AFTER"
	# parameters["val_0"] = 

	# parameters["operation"] = "BEFORE"
	# parameters["val_0"] = 

	# parameters["operation"] = "IN_RANGE"
	# parameters["val_0"] = 
	# parameters["val_1"] = 

	def __init__(self, parameters):
		self.parameters = parameters

	def eventTriggered(self):
		import random

		if parameters["operation"] == "TEMPERATURE_IN_RANGE":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))

		elif parameters["operation"] == "CHECK_SUNNY":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))

		elif parameters["operation"] == "CHECK_RAINY":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))

		elif parameters["operation"] == "CHECK_CLOUDY":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))


		else:
			raise UnsupportedDriverParameterError()


	def __str__(self):
		return "WeatherTriggerDriver: "
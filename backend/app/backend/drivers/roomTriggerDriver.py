import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class RoomTriggerDriver(GenericTriggerDriver):


	# parameters = {}

	# parameters["operation"] = "AFTER"
	# parameters["val_0"] = 


	def __init__(self, parameters):
		self.parameters = parameters

	
	def eventTriggered(self):

		import random

		if self.parameters["operation"] == "CHECK_PRESENCE":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))


		elif self.parameters["operation"] == "CHECK_ABSENCE":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TEMPERATURE_IN_RANGE":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))

		
		else:
			raise UnsupportedDriverParameterError()


	def __str__(self):
		return "RoomTriggerDriver: "
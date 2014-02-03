import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class DatetimeTriggerDriver(GenericTriggerDriver):


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

		if self.parameters["operation"] == "DATE_IN_RANGE":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TIME_IN_RANGE":
			
			print "TODO to be implemented"
			return bool(random.getrandbits(1))


		else:
			raise UnsupportedDriverParameterError()


	def __str__(self):
		return "DatetimeTriggerDriver: "
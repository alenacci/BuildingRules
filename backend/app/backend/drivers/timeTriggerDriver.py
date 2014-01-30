import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class TimeTriggerDriver(GenericTriggerDriver):


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
		pass

	def __str__(self):
		return "TimeTriggerDriver: "
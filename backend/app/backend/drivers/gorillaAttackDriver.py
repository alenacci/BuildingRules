############################################################
#
# BuildingRules Project 
# Politecnico di Milano
# Author: Alessandro A. Nacci
#
# This code is confidential
# Milan, March 2014
#
############################################################

import sys
import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver
import imp
import os

trigger = imp.load_source("requestHelper",os.path.join(os.path.dirname(__file__), '../../../../apps/dangerProject/VirtualSensor/tools/requestHelper.py'))

class GorillaAttackDriver(GenericTriggerDriver):


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

	def __simulatedEventTriggered(self):
		import random

		if self.parameters["operation"] == "GORILLA_ATTACK":
			
			return True
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __actualEventTriggered(self):
		import random

		if self.parameters["operation"] == "GORILLA_ATTACK":
			#Check the virtual sensor
			status = trigger.check_sensor_status()
			if status['status'] == 'True':
				self.parameters["returnValues"] = status
				return True
			else:
				return False
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedEventTriggeredWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		return self.__simulatedEventTriggered()


	def eventTriggered(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedEventTriggeredWrapper()
		return self.__actualEventTriggered()


	def __str__(self):
		return "FakeTriggerDriver: "
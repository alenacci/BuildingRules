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
import os
import imp

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

trigger = imp.load_source('bulletin', os.path.join(os.path.dirname(__file__), '../../../../apps/dangerProject/DangerCore/tools/triggerRequestHelper.py'))


"""Check if a real Danger is triggered. In our implementation it waits for the building
	manager to confirm the danger"""
class DangerTriggerDriver(GenericTriggerDriver):


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
		return True


	def __actualEventTriggered(self):


		trigger_name = self.parameters["operation"]
		room_name = self.parameters["roomName"]
		building_name = self.parameters["buildingName"]
		print ("check for " + trigger_name)
		status = trigger.check_trigger_status(trigger_name,building_name,room_name)
		print ("Status is " + str(status))
		return status


	def __simulatedEventTriggeredWrapper(self):
		#print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]",
		return self.__simulatedEventTriggered()


	def eventTriggered(self):
		#if 'simulationParameters' in self.parameters:
		#	return self.__simulatedEventTriggeredWrapper()
		return self.__actualEventTriggered()


	def __str__(self):
		return "FakeTriggerDriver: "
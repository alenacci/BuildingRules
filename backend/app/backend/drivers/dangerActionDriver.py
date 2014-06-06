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

from app.backend.commons.errors import *
from app.backend.commons.simulation import writeSimulationLog

import imp
bulletin = imp.load_source('bulletin', os.path.join(os.path.dirname(__file__), '../../../../apps/dangerProject/DangerCore/tools/bulletin.py'))

"""This driver is set to start after the trigger "GORILLA IS COMING". Name to change
	and send the bulletin to the dangerCore, which probably will notify the building manager"""
class DangerActionDriver:

	def __init__(self, parameters):
		self.parameters = parameters


	def __actualActuation(self):
		operation = self.parameters['operation']
		try:
			print "room: " + self.parameters['danger_room']
		except Exception,e :
			print("error: " + str(e))
		print "send bulletin!!!"
		bulletin.send_bulletin( danger_type=operation, building=self.parameters['buildingName'], room=self.parameters['roomName'])

	def __simulatedActuation(self):
		pass

	def __simulatedActuationWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		self.__simulatedActuation()

	def actuate(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedActuationWrapper()

		return self.__actualActuation()

	def __str__(self):
		return "LightActionDriver: "
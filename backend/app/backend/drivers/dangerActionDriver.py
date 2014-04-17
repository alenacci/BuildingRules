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
from app.backend.commons.simulation import writeSimulationLog

import imp
bulletin = imp.load_source('bulletin', '/home/danger/Danger/dangerProject/DangerCore/tools/bulletin.py')


class DangerActionDriver:

	def __init__(self, parameters):
		self.parameters = parameters


	def __actualActuation(self):
		operation = parameters['operation']
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
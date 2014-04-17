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



class AlarmActionDriver:

	def __init__(self, parameters):
		self.parameters = parameters


	def __actualActuation(self):
		print "ALARM!!!"


	def __simulatedActuation(self):
		print "ALARM!!!"

	def __simulatedActuationWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		self.__simulatedActuation()

	def actuate(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedActuationWrapper()

		return self.__actualActuation()

	def __str__(self):
		return "LightActionDriver: "
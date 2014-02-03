import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericActionDriver import GenericActionDriver

class RoomActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def actuate(self):

		if self.parameters["operation"] == "LIGHT_ON":			
			print "TODO to be implemented"
	
		elif self.parameters["operation"] == "LIGHT_OFF":		
			print "TODO to be implemented"
			
		elif self.parameters["operation"] == "HEATING_ON":		
			print "TODO to be implemented"

		elif self.parameters["operation"] == "HEATING_OFF":		
			print "TODO to be implemented"

		elif self.parameters["operation"] == "COOLING_ON":		
			print "TODO to be implemented"

		elif self.parameters["operation"] == "COOLING_OFF":		
			print "TODO to be implemented"

		elif self.parameters["operation"] == "WINDOWS_CLOSE":		
			print "TODO to be implemented"

		elif self.parameters["operation"] == "CURTAINS_OPEN":		
			print "TODO to be implemented"
			
		elif self.parameters["operation"] == "CURTAINS_CLOSE":		
			print "TODO to be implemented"

		else:
			raise UnsupportedDriverParameterError()


	def __str__(self):
		return "RoomActionDriver: "


	

	




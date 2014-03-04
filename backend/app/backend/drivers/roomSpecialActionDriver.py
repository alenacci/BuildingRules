import sys
import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericActionDriver import GenericActionDriver

class RoomSpecialActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def actuate(self):


		if self.parameters["operation"] == "SEND_COMPLAIN":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __str__(self):
		return "RoomActionDriver: "


	

	




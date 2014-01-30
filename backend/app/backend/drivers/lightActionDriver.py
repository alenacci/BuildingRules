import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.drivers.genericActionDriver import GenericActionDriver

class LightActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def actuate(self):
		pass

	def __str__(self):
		return "LightActionDriver: "
import sys
import json
import random
import string
import datetime

from app.backend.commons.errors import *

class GenericActionDriver:

	def __init__(self, parameters):
		self.parameters = parameters

	def actuate(self):
		pass

	def __str__(self):
		return "LightActionDriver: "
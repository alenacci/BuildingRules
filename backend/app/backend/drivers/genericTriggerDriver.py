import sys
import json
import random
import string
import datetime

from app.backend.commons.errors import *

class GenericTriggerDriver:

	def __init__(self, parameters):
		self.parameters = parameters

	def eventTriggered(self):
		pass

	def __str__(self):
		return "TimeTriggerDriver: "
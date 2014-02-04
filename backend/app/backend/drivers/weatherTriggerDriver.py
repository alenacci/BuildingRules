import sys
import json
import random
import string
import datetime
import urllib2

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver


class WeatherTriggerDriver(GenericTriggerDriver):


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
		self.__WEATHER_SERVICE_FILE_PATH = "tools/weather/"

	def eventTriggered(self):
	
		text = ""
		try:
			in_file = open(self.__WEATHER_SERVICE_FILE_PATH + "weather.json","r")
			text = in_file.read()
			in_file.close()			
		except:
			try:
				in_file = open(self.__WEATHER_SERVICE_FILE_PATH + "weather.json","r")
				text = in_file.read()
				in_file.close()
			except:
				raise WeatherInfoError("Impossible to retrieve weather information")

		weather = json.loads(text)


		if self.parameters["operation"] == "TEMPERATURE_IN_RANGE":

			currentScale = ""
			if 'C' in self.parameters['0'].upper(): 
				currentScale = 'C'
			elif 'F' in self.parameters['0'].upper(): 
				currentScale = 'F'
			else:
				raise WeatherInfoError("Unsupported temperature scale")
	
			kelvinTemp = float(weather["main"]["temp"])
			
			if currentScale == "F":
				convTemp = ((kelvinTemp - 273) * 1.8 ) + 32;
			elif currentScale == "C":
				convTemp = (kelvinTemp - 273);
			else:
				raise WeatherInfoError("Unsopported temperature scale parameter")
			
			if convTemp >= float(self.parameters['0'].upper().replace(currentScale, "").strip()) and convTemp <= float(self.parameters['1'].upper().replace(currentScale, "").strip()):
				return True
			else:
				return False

		elif self.parameters["operation"] == "CHECK_SUNNY":
			return True if weather["weather"][0]["main"].upper() == "CLEAR" else False

		elif self.parameters["operation"] == "CHECK_RAINY":
			return True if weather["weather"][0]["main"].upper() == "RAIN" else False

		elif self.parameters["operation"] == "CHECK_CLOUDY":
			return True if weather["weather"][0]["main"].upper() == "CLOUDS" else False


		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __str__(self):
		return "WeatherTriggerDriver: "
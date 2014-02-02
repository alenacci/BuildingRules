import json
import random
import string
import datetime
import re

from app.backend.commons.errors import *
from app.backend.model.trigger import Trigger
from app.backend.model.triggers import Triggers

class TriggerManager:

	def __init__(self):
		pass

	def getInfo(self, triggerName):
	
		trigger = Action(triggerName = triggerName)
		trigger.retrive()
		return trigger.getDict()


	def getTriggerAndTemplateAndParameterValues(self, ruleAntecedent):

		triggers = Triggers()
		triggerList = triggers.getAllTriggers()

		for trigger in triggerList:
			
			# A trigger.ruleAntecedent is represented as set of templates models:
			# Example "template1 | template2 | template2"
			# Where each template can be like
			# "it is between %d AM and %d AM | it is between %d AM and %d PM | it is between %d PM and %d AM | it is between %d PM and %d PM"

			models = trigger.ruleAntecedent.split('|')

			for model in models:
				parameterNumber = model.count("@val")
				originalModel = model.strip()
				model = model.replace("@val","(.+)").strip()

				matchObj = re.match( model, ruleAntecedent, re.M|re.I)

				if matchObj:
					parameterValues = {}

					for i in range(0,parameterNumber):
						parameterValues[str(i)] = matchObj.group(i + 1)

					return (trigger, originalModel, parameterValues)

		raise NotWellFormedRuleError("Impossible to find any trigger corresponding to the following rule consequent > " + ruleAntecedent)


	def getTriggerAndTemplate(self, ruleAntecedent):
		trigger, template, parameterValues = self.getTriggerAndTemplateAndParameterValues(ruleAntecedent)
		return (trigger, template)

	def getTrigger(self, ruleAntecedent):

		trigger, template = self.getTriggerAndTemplate(ruleAntecedent)
		return trigger

	def __translateParameters(self, triggerCategory, parameterValue):

		value = parameterValue

		if triggerCategory == "TIME":
			
			pm = False
			if "PM" in value.upper():
				pm = True
			
			if "." in value or ":" in value:
				value = value.replace(":",".")
				value = value[:value.find(".")]
			
			return value.replace("AM", "").replace("PM", "").replace("am", "").replace("pm", "")

			if pm: value = str(int(value)+12)

		if triggerCategory == "DATE":
			import time
			day = value[:value.find("/")]
			month = value[value.find("/")+1:]
			return str( time.strptime(day + " " + month + " 00", "%d %m %y").tm_yday )

		if triggerCategory == "ROOM_TEMPERATURE" or triggerCategory == "ROOM_TEMPERATURE":
			return value.replace("C", "").replace("F", "")

		return value


	def translateTrigger(self, ruleAntecedent):

		triggers = Triggers()
		trigger, originalTemplate, parameterValues = self.getTriggerAndTemplateAndParameterValues(ruleAntecedent)
		translationTemplate = triggers.translateTemplate('Z3', originalTemplate)

		translatedParams = {}

		for key,value in parameterValues.iteritems():
			translatedParams[key] = self.__translateParameters(trigger.category, value)

		translation = translationTemplate
		for i in range(0,len(parameterValues.keys())):

			value = translatedParams[str(i)]
			translation = translation.replace("@val", value, 1)

		return translation, trigger, translatedParams


	def getTriggerCategories(self):
		
		triggers = Triggers()
		triggerList = triggers.getAllTriggers()

		categories = []
		for trigger in triggerList:
			if trigger.category not in categories:
				categories.append(trigger.category)

		return categories


	def getTriggerDriver(self, trigger, parameters = None):

		from app.backend.drivers.datetimeTriggerDriver import DatetimeTriggerDriver
		from app.backend.drivers.roomTriggerDriver import RoomTriggerDriver
		from app.backend.drivers.weatherTriggerDriver import WeatherTriggerDriver
		from app.backend.drivers.fakeTriggerDriver import FakeTriggerDriver

		if not parameters:
			parameters = {}

		driver = None

		if trigger.triggerName == "OCCUPANCY_TRUE":
			driver = RoomTriggerDriver(parameters.update({'operation' : 'CHECK_PRESENCE'}))

		if trigger.triggerName == "OCCUPANCY_FALSE":
			driver = RoomTriggerDriver(parameters.update({'operation' : 'CHECK_ABSENCE'}))

		if trigger.triggerName == "ROOM_TEMPERATURE_RANGE":
			driver = RoomTriggerDriver(parameters.update({'operation' : 'TEMPERATURE_IN_RANGE'}))

		if trigger.triggerName == "TIME_RANGE":
			driver = DatetimeTriggerDriver(parameters.update({'operation' : 'TIME_IN_RANGE'}))

		if trigger.triggerName == "DATE_RANGE":
			driver = DatetimeTriggerDriver(parameters.update({'operation' : 'DATE_IN_RANGE'}))

		if trigger.triggerName == "EXT_TEMPERATURE_RANGE":
			driver = WeatherTriggerDriver(parameters.update({'operation' : 'TEMPERATURE_IN_RANGE'}))

		if trigger.triggerName == "SUNNY":
			driver = WeatherTriggerDriver(parameters.update({'operation' : 'CHECK_SUNNY'}))

		if trigger.triggerName == "NO_RULE":
			driver = FakeTriggerDriver(parameters.update({'operation' : 'NO_RULE'}))

		if not driver:
			raise DriverNotFoundError("Impossibile to find any driver for the trigger " + str(trigger))


	def __str__(self):
		return "ActionManager: "
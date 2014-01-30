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
					parameterValues = []

					for i in range(0,parameterNumber):
						parameterValues.append(matchObj.group(i + 1))

					return (trigger, originalModel, parameterValues)

		raise NotWellFormedRuleError("Impossible to find any trigger corresponding to the following rule consequent > " + ruleAntecedent)


	def getTriggerAndTemplate(self, ruleAntecedent):
		trigger, template, parameterValues = self.getTriggerAndTemplateAndParameterValues(ruleAntecedent)
		return (trigger, template)

	def getTrigger(self, ruleAntecedent):

		trigger, template = self.getTriggerAndTemplate(ruleAntecedent)
		return trigger

	def translateTrigger(self, ruleAntecedent):

		triggers = Triggers()
		trigger, originalTemplate, parameterValues = self.getTriggerAndTemplateAndParameterValues(ruleAntecedent)
		translationTemplate = triggers.translateTemplate('Z3', originalTemplate)

		foundValues = parameterValues

		translation = translationTemplate
		for value in foundValues:
			translation = translation.replace("@val", value, 1)

		return translation


	def getTriggerCategories(self):
		
		triggers = Triggers()
		triggerList = triggers.getAllTriggers()

		categories = []
		for trigger in triggerList:
			if trigger.category not in categories:
				categories.append(trigger.category)

		return categories


	def getTriggerDriver(self, trigger):

		from app.backend.drivers.timeTriggerDriver import TimeTriggerDriver


		if trigger.triggerName == "TIME_AFTER":
			driver = TimeTriggerDriver(parameters = {'operation' : 'AFTER'})

		if trigger.triggerName == "TIME_BEFORE":
			driver = TimeTriggerDriver(parameters = {'operation' : 'BEFORE'})

		if trigger.triggerName == "TIME_RANGE":
			driver = TimeTriggerDriver(parameters = {'operation' : 'IN_RANGE'})

		raise DriverNotFoundError("Impossibile to find any driver for the trigger " + str(trigger))


	def __str__(self):
		return "ActionManager: "
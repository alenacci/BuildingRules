import json
import random
import string
import datetime

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


	def getTrigger(self, ruleAntecedent):

		triggers = Triggers()
		triggerList = triggers.getAllTriggers()

		for trigger in triggerList:
			
			# A trigger.ruleAntecedent is represented as set of templates models:
			# Example "template1 | template2 | template2"
			# Where each template can be like
			# "it is between %d AM and %d AM | it is between %d AM and %d PM | it is between %d PM and %d AM | it is between %d PM and %d PM"

			# Each template is composed by different parts delimited by the different %d
			# SO the template "it is between %d AM and %d AM" is made of "part0 %d part1 %d part2"

			models = trigger.ruleAntecedent.split('|')

			for model in models:
				parts = model.split("@val")

				matches = 0
				target = ruleAntecedent
				for part in parts:
					if part in target:
						target = target.replace(part, "")
						matches += 1

				if matches == len(parts):
					return trigger

		raise NotWellFormedRuleError("Impossible to find any trigger corresponding to the following rule consequent > " + ruleAntecedent)

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
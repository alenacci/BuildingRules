import json
import random
import string
import datetime

from app.backend.commons.errors import *
from app.backend.model.action import Action
from app.backend.model.actions import Actions

class ActionManager:

	def __init__(self):
		pass

	def getInfo(self, actionName):
	
		action = Action(actionName = actionName)
		action.retrive()
		return action.getDict()


	def getActionAndTemplate(self, ruleConsequent):

		actions = Actions()
		actionList = actions.getAllActions()

		for action in actionList:
			
			# A action.ruleConsequent is represented as set of templates models:
			# Example "template1 | template2 | template2"

			# Each template is composed by different parts delimited by the different %d
			# Example "part0 %d part1 %d part2"

			models = action.ruleConsequent.split('|')

			for model in models:
				parts = model.split("@val")

				matches = 0
				target = ruleConsequent
				for part in parts:
					if part in target:
						target = target.replace(part, "")
						matches += 1

				if matches == len(parts):
					return (action, model)

		raise NotWellFormedRuleError("Impossible to find any action corresponding to the following rule consequent > " + ruleConsequent)

	def getAction(self, ruleConsequent):
		
		action, template = self.getActionAndTemplate(ruleConsequent)
		return action


	def getActionCategories(self):
		
		actions = Actions()
		actionList = actions.getAllActions()

		categories = []
		for action in actionList:
			if action.category not in categories:
				categories.append(action.category)

		return categories


	def getActionDriver(self, action):

		from app.backend.drivers.lightActionDriver import LightActionDriver


		if action.actionName == "LIGHT_ON":
			driver = LightActionDriver(parameters = {'operation' : 'LIGHT_ON'})

		if action.actionName == "LIGHT_OFF":
			driver = LightActionDriver(parameters = {'operation' : 'LIGHT_OFF'})

		raise DriverNotFoundError("Impossibile to find any driver for the action " + str(action))


	def __str__(self):
		return "ActionManager: "
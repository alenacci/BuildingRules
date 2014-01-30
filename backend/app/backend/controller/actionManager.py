import json
import random
import string
import datetime
import re

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


	def getActionAndTemplateAndParameterValues(self, ruleConsequent):

		actions = Actions()
		actionList = actions.getAllActions()

		for action in actionList:
			
			# A action.ruleConsequent is represented as set of templates models:
			# Example "template1 | template2 | template2"

			models = action.ruleConsequent.split('|')

			for model in models:
				parameterNumber = model.count("@val")
				originalModel = model.strip()
				model = model.replace("@val","(.+)").strip()

				matchObj = re.match( model, ruleConsequent, re.M|re.I)

				if matchObj:
					parameterValues = []

					for i in range(0,parameterNumber):
						parameterValues.append(matchObj.group(i + 1))

					return (action, originalModel, parameterValues)

		raise NotWellFormedRuleError("Impossible to find any action corresponding to the following rule consequent > " + ruleConsequent)


	def getActionAndTemplate(self, ruleConsequent):
		action, template, parameterValues = self.getActionAndTemplateAndParameterValues(ruleConsequent)
		return (action, template)

	def getAction(self, ruleConsequent):

		action, template = self.getActionAndTemplate(ruleConsequent)
		return action

	def translateAction(self, ruleConsequent):

		triggers = Triggers()
		trigger, originalTemplate, parameterValues = self.getTriggerAndTemplateAndParameterValues(ruleConsequent)
		translationTemplate = triggers.translateTemplate('Z3', originalTemplate)

		foundValues = parameterValues

		translation = translationTemplate
		for value in foundValues:
			translation = translation.replace("@val", value, 1)

		return translation



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
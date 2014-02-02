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

		actions = Actions()
		action, originalTemplate, parameterValues = self.getActionAndTemplateAndParameterValues(ruleConsequent)
		translationTemplate = actions.translateTemplate('Z3', originalTemplate)

		translation = translationTemplate

		return translation, action



	def getActionCategories(self):
		
		actions = Actions()
		actionList = actions.getAllActions()

		categories = []
		for action in actionList:
			if action.category not in categories:
				categories.append(action.category)

		return categories


	def getActionDriver(self, action, parameters = None):

		from app.backend.drivers.lightActionDriver import RoomActionDriver

		if not parameters:
			parameters.update()

		driver = None

		if action.actionName == "LIGHT_ON":
			driver = RoomActionDriver(parameters.update({'operation' : 'LIGHT_ON'}))

		if action.actionName == "LIGHT_OFF":
			driver = RoomActionDriver(parameters.update({'operation' : 'LIGHT_OFF'}))

		if action.actionName == "HEATING_ON":
			driver = RoomActionDriver(parameters.update({'operation' : 'HEATING_ON'}))

		if action.actionName == "HEATING_OFF":
			driver = RoomActionDriver(parameters.update({'operation' : 'HEATING_OFF'}))

		if action.actionName == "COOLING_ON":
			driver = RoomActionDriver(parameters.update({'operation' : 'COOLING_ON'}))

		if action.actionName == "COOLING_OFF":
			driver = RoomActionDriver(parameters.update({'operation' : 'COOLING_OFF'}))

		if action.actionName == "WINDOWS_OPEN":
			driver = RoomActionDriver(parameters.update({'operation' : 'WINDOWS_OPEN'}))

		if action.actionName == "WINDOWS_CLOSE":
			driver = RoomActionDriver(parameters.update({'operation' : 'WINDOWS_CLOSE'}))

		if action.actionName == "CURTAINS_OPEN":
			driver = RoomActionDriver(parameters.update({'operation' : 'CURTAINS_OPEN'}))

		if action.actionName == "CURTAINS_CLOSE":
			driver = RoomActionDriver(parameters.update({'operation' : 'CURTAINS_CLOSE'}))

		if not driver:
			raise DriverNotFoundError("Impossibile to find any driver for the action " + str(action))


	def __str__(self):
		return "ActionManager: "
import sys
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
					parameterValues = {}

					for i in range(0,parameterNumber):
						parameterValues[str(i)] = matchObj.group(i + 1)

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

		from app.backend.drivers.roomActionDriver import RoomActionDriver

		if not parameters:
			parameters = {}

		if action.actionName == "LIGHT_ON":
			parameters.update({'operation' : 'LIGHT_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "LIGHT_OFF":
			parameters.update({'operation' : 'LIGHT_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "HEATING_ON":
			parameters.update({'operation' : 'HEATING_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "HEATING_OFF":
			parameters.update({'operation' : 'HEATING_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "COOLING_ON":
			parameters.update({'operation' : 'COOLING_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "COOLING_OFF":
			parameters.update({'operation' : 'COOLING_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "WINDOWS_OPEN":
			parameters.update({'operation' : 'WINDOWS_OPEN'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "WINDOWS_CLOSE":
			parameters.update({'operation' : 'WINDOWS_CLOSE'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "CURTAINS_OPEN":
			parameters.update({'operation' : 'CURTAINS_OPEN'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "CURTAINS_CLOSE":
			parameters.update({'operation' : 'CURTAINS_CLOSE'})
			return  RoomActionDriver(parameters = parameters)

		
		raise DriverNotFoundError("Impossibile to find any driver for the action " + str(action))


	def __str__(self):
		return "ActionManager: "
import sys
import json
import random
import string
import datetime
import re

from app.backend.commons.errors import *
from app.backend.commons.inputDataChecker import checkData
from app.backend.model.action import Action
from app.backend.model.actions import Actions

class ActionManager:

	def __init__(self):
		pass

	def getInfo(self, actionName):
		checkData(locals())
	
		action = Action(actionName = actionName)
		action.retrive()
		return action.getDict()


	def getActionAndTemplateAndParameterValues(self, ruleConsequent):
		checkData(locals())

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
		checkData(locals())

		action, template, parameterValues = self.getActionAndTemplateAndParameterValues(ruleConsequent)
		return (action, template)

	def getAction(self, ruleConsequent):
		checkData(locals())

		action, template = self.getActionAndTemplate(ruleConsequent)
		return action

	def __translateParameters(self, actionCategory, parameterValue):

		value = parameterValue

		if actionCategory == "HVAC_TEMP":
			return value.replace("C", "").replace("F", "")

		if actionCategory == "HVAC_HUM":
			return value.replace("%", "")

		return value



	def translateAction(self, ruleConsequent):
		checkData(locals())

		actions = Actions()
		action, originalTemplate, parameterValues = self.getActionAndTemplateAndParameterValues(ruleConsequent)
		translationTemplate = actions.translateTemplate('Z3', originalTemplate)

		translatedParams = {}

		for key,value in parameterValues.iteritems():
			translatedParams[key] = self.__translateParameters(action.category, value)


		translation = translationTemplate

		for i in range(0,len(parameterValues.keys())):

			value = translatedParams[str(i)]
			translation = translation.replace("@val", value, 1)


		return translation, action, translatedParams



	def getActionCategories(self):
		checkData(locals())

		
		actions = Actions()
		actionList = actions.getAllActions()

		categories = []
		for action in actionList:
			if action.category not in categories:
				categories.append(action.category)

		return categories


	def getActionDriver(self, action, parameters = None):
		checkData(locals())

		from app.backend.drivers.roomActionDriver import RoomActionDriver

		if not parameters:
			parameters = {}

		if action.actionName == "LIGHT_ON":
			parameters.update({'operation' : 'LIGHT_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "LIGHT_OFF":
			parameters.update({'operation' : 'LIGHT_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "HVAC_ON":
			parameters.update({'operation' : 'HVAC_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "HVAC_OFF":
			parameters.update({'operation' : 'HVAC_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "SET_TEMPERATURE":
			parameters.update({'operation' : 'SET_TEMPERATURE'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "SET_HUMIDITY":
			parameters.update({'operation' : 'SET_HUMIDITY'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "COFFEE_ON":
			parameters.update({'operation' : 'COFFEE_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "COFFEE_OFF":
			parameters.update({'operation' : 'COFFEE_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "PRINTER_ON":
			parameters.update({'operation' : 'PRINTER_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "PRINTER_OFF":
			parameters.update({'operation' : 'PRINTER_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "COMPUTER_ON":
			parameters.update({'operation' : 'COMPUTER_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "COMPUTER_OFF":
			parameters.update({'operation' : 'COMPUTER_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "DESKLIGHT_ON":
			parameters.update({'operation' : 'DESKLIGHT_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "DESKLIGHT_OFF":
			parameters.update({'operation' : 'DESKLIGHT_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "DISPLAYMONITOR_ON":
			parameters.update({'operation' : 'DISPLAYMONITOR_ON'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "DISPLAYMONITOR_OFF":
			parameters.update({'operation' : 'DISPLAYMONITOR_OFF'})
			return  RoomActionDriver(parameters = parameters)

		if action.actionName == "SEND_COMPLAIN":
			parameters.update({'operation' : 'DISPLAYMONITOR_OFF'})
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
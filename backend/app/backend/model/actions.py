import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database
from app.backend.model.action import Action

class Actions:
	def __init__(self):
		pass

	def getAllActions(self):

		actionList = []

		database = Database()
		database.open()
		query = "SELECT * FROM actions;"
		queryResult = database.executeReadQuery(query)

		for record in queryResult:
			actionId = record[0]
			category = record[1]
			actionName = record[2]
			ruleConsequent = record[3]
			description = record[4]

			action = Action(id = actionId, category = category, actionName = actionName, ruleConsequent = ruleConsequent, description = description)
			actionList.append(action)

		database.close()		

		return actionList

	def __str__(self):
		return "Actions: "
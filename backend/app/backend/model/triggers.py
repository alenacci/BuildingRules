import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database
from app.backend.model.trigger import Trigger

class Triggers:
	def __init__(self):
		pass

	def getAllTriggers(self):

		triggerList = []

		database = Database()
		database.open()
		query = "SELECT * FROM triggers;"
		queryResult = database.executeReadQuery(query)

		for record in queryResult:
			triggerId = record[0]
			category = record[1]
			triggerName = record[2]
			ruleAntecedent = record[3]
			description = record[4]

			trigger = Trigger(id = triggerId, category = category, triggerName = triggerName, ruleAntecedent = ruleAntecedent, description = description)
			triggerList.append(trigger)

		database.close()		

		return triggerList

	def __str__(self):
		return "Triggers: "
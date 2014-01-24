import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Action:
	def __init__(self, id = None, actionName = None, ruleConsequent = None, description = None):

			self.id = id
			self.actionName = actionName
			self.ruleConsequent = ruleConsequent
			self.description = description

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 				!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.actionName 		!= None	: 	queryTemplate = queryTemplate.replace("@@action_name@@", self.actionName)
		if self.ruleConsequent	!= None	: 	queryTemplate = queryTemplate.replace("@@rule_consequent@@", self.ruleConsequent)
		if self.description		!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM actions WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE actions SET action_name = '@@action_name@@', rule_consequent = '@@rule_consequent@@', description = '@@description@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO actions (action_name, rule_consequent, description) VALUES ('@@action_name@@', '@@rule_consequent@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		database = Database()
		database.open()

		query = "SELECT * FROM actions WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.id = queryResult[0][0]
			self.actionName = queryResult[0][1]
			self.ruleConsequent = queryResult[0][2]
			self.description = queryResult[0][3]
		else:
			database.close()
			raise ActionNotFoundError("Impossibile to find any action with the provided values")


		database.close()


	def delete(self):

		print "TODO: Consistency check not performed - Action class"

		database = Database()
		database.open()

		query = "DELETE FROM actions WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["actionName"] = self.actionName
		response["ruleConsequent"] = self.ruleConsequent
		response["description"] = self.description

		return response	

	def __str__(self):
		return "Trigger: " + str(self.id) + " " + str(self.triggerName) + " " + str(self.ruleConsequent) + " " + str(self.description)
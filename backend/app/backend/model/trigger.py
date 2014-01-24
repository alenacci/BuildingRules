import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Trigger:
	def __init__(self, id = None, triggerName = None, ruleAntecedent = None, description = None):

			self.id = id
			self.triggerName = triggerName
			self.ruleAntecedent = ruleAntecedent
			self.description = description

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 				!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.triggerName 	!= None	: 	queryTemplate = queryTemplate.replace("@@trigger_name@@", self.triggerName)
		if self.ruleAntecedent	!= None	: 	queryTemplate = queryTemplate.replace("@@rule_antecedent@@", self.ruleAntecedent)
		if self.description		!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM triggers WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE triggers SET trigger_name = '@@trigger_name@@', rule_consequent = '@@rule_consequent@@', description = '@@description@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO triggers (trigger_name, rule_consequent, description) VALUES ('@@trigger_name@@', '@@rule_consequent@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		database = Database()
		database.open()

		query = "SELECT * FROM triggers WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.id = queryResult[0][0]
			self.triggerName = queryResult[0][1]
			self.ruleAntecedent = queryResult[0][2]
			self.description = queryResult[0][3]
		else:
			database.close()
			raise TriggerNotFoundError("Impossibile to find any trigger with the provided values")

		database.close()

	def delete(self):

		print "TODO: Consistency check not performed - Trigger class"

		database = Database()
		database.open()

		query = "DELETE FROM triggers WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["triggerName"] = self.triggerName
		response["ruleAntecedent"] = self.ruleAntecedent
		response["description"] = self.description

		return response	


	def __str__(self):
		return "Trigger: " + str(self.id) + " " + str(self.triggerName) + " " + str(self.ruleAntecedent) + " " + str(self.description)
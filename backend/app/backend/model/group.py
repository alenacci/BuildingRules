import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Group:
	def __init__(self, id = None, buildingName = None, description = None):

			self.id = id
			self.buildingName = buildingName
			self.description = description

	def getBuilding(self):
		from app.backend.model.building import Building

		building = Building(buildingName = self.buildingName)
		building.retrieve()
		return building


	def getRooms(self):
		print "TODO: non yet tested"
		
		from app.backend.model.room import Room

		database = Database()
		database.open()

		query = "SELECT * FROM rooms_groups WHERE group_id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		roomList = []
		for record in queryResult:
			buildingName = record[1]
			roomName = record[2]
			
			room = Room(roomName = roomName,  buildingName = buildingName)
			room.retrieve()

			roomList.append(room)

		return roomList


	def getRules(self, excludedRuleId = False):		

		from app.backend.model.rule import Rule

		query = "SELECT id FROM rules WHERE group_id = '@@id@@' @@__EXCLUDED_RULE_ID__@@;"

		if excludedRuleId:
			query = query.replace("@@__EXCLUDED_RULE_ID__@@", "AND NOT id = " + str(excludedRuleId))
		else:
			query = query.replace("@@__EXCLUDED_RULE_ID__@@", "")


		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		
		ruleList = []
		for ruleRecord in queryResult:
			rule = Rule(ruleRecord[0])
			rule.retrieve()
			ruleList.append(rule)

		return ruleList


	def addRule(self, rule):

		rule.groupId = self.id
		rule.buildingName = self.buildingName
		rule.store()

		return rule


	def addRoom(self, room):
		database = Database()
		database.open()

		query = "INSERT INTO rooms_groups (group_id, building_name, room_name) VALUES ('@@id@@', '@@building_name@@', '@@room_name@@');"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@room_name@@", str(room.roomName))
		database.executeWriteQuery(query)

		database.close()


	def deleteRoom(self, room):
		database = Database()
		database.open()

		query = "DELETE FROM rooms_groups WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@' AND group_id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@room_name@@", str(room.roomName))
		database.executeWriteQuery(query)

		database.close()

	def deleteRule(self, rule):
		rule.delete()

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 				!= None	:	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.buildingName 	!= None	: 	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.description 	!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):
		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM groups WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE groups SET description = '@@description@@' WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		else:
			query = "INSERT INTO groups (building_name, description) VALUES ('@@building_name@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		self.id = int(database.getLastInsertedId()) if not self.id else self.id
		database.close()


	def retrieve(self):

		if not(self.id and self.buildingName):
			raise Exception("Group querying required both group id and buildingName")

		database = Database()
		database.open()

		query = "SELECT * FROM groups WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.id = int(queryResult[0][0])
			self.buildingName = queryResult[0][1]
			self.description = queryResult[0][2]
		else:
			database.close()
			raise Exception("Impossibile to find any group with the provided values")

		database.close()


	def delete(self):
		print "TODO: Consistency check not performed - Group class"

		database = Database()
		database.open()

		query = "DELETE FROM groups WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["buildingName"] = self.buildingName
		response["description"] = self.description

		return response	


	def __str__(self):
		return "Group: " + str(self.id) + " - " + str(self.buildingName) + " - " + str(self.description)
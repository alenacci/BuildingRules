import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database


class Room:
	def __init__(self, roomName = None,  buildingName = None, description = None):
		
		self.roomName = roomName
		self.buildingName = buildingName
		self.description = description


	def getActions(self):
		print "TODO: non yet tested"

		from app.backend.model.action import Action

		database = Database()
		database.open()

		query = "SELECT * FROM rooms_actions WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		actionList = []
		for record in queryResult:
			actionId = record[2]
			
			action = Action(id = actionId)
			action.retrieve()

			actionList.append(action)

		return actionList


	def getTriggers(self):
		print "TODO: non yet tested"

		from app.backend.model.trigger import Trigger

		database = Database()
		database.open()

		query = "SELECT * FROM rooms_triggers WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		triggerList = []
		for record in queryResult:
			triggerId = record[2]
			
			trigger = Trigger(id = triggerId)
			trigger.retrieve()

			triggerList.append(trigger)

		return triggerList

	def addAction(self, action):

		print "TODO: non yet tested"

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "INSERT INTO rooms_actions (room_name, building_name, action_id) VALUES ('@@room_name@@', '@@building_name@@', '@@action_id@@');"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@action_id@@", str(action.id))
		database.executeWriteQuery(query)

		database.close()


	def deleteAction(self, action):
		print "TODO: non yet tested"		

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "DELETE FROM rooms_actions WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@' AND action_id = '@@action_id@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@action_id@@", str(action.id))
		database.executeWriteQuery(query)

		database.close()


	def addTrigger(self, trigger):
		print "TODO: non yet tested"

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "INSERT INTO rooms_triggers (room_name, building_name, trigger_id) VALUES ('@@room_name@@', '@@building_name@@', '@@trigger_id@@');"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@trigger_id@@", str(trigger.id))
		database.executeWriteQuery(query)

		database.close()


	def deleteTrigger(self, trigger):
		print "TODO: non yet tested"		

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "DELETE FROM rooms_triggers WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@' AND trigger_id = '@@trigger_id@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@trigger_id@@", str(trigger.id))
		database.executeWriteQuery(query)

		database.close()		


	def getUsers(self):

		print "TODO: non yet tested"

		from app.backend.model.user import User

		database = Database()
		database.open()

		query = "SELECT * FROM users_rooms WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		userList = []
		for record in queryResult:
			uuid = record[2]

			user = User(uuid = uuid)
			user.retrieve()

			userList.append(user)

		return userList


	def getBuilding(self):
		from app.backend.model.building import Building

		building = Building(buildingName = self.buildingName)
		building.retrieve()
		return building

	def getGroups(self):

		print "TODO: non yet tested"

		from app.backend.model.group import Group

		database = Database()
		database.open()

		query = "SELECT * FROM rooms_groups WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		groupList = []
		for record in queryResult:
			groupId = record[0]
			buildingName = record[1]
			
			group = Group(id = groupId,  buildingName = buildingName)
			group.retrieve()

			groupList.append(group)

		return groupList

	def getRules(self, author = None, includeGroupsRules = False, excludedRuleId = False, excludeCrossRoomValidationRules = False):

		print "TODO: this method has been partially tested - includeGroupsRules not tested"

		from app.backend.model.rule import Rule
		
		if author:
			query = "SELECT id FROM rules WHERE room_name = '@@room_name@@' AND author_uuid = '@@author_uuid@@' @@__EXCLUDED_RULE_ID__@@;"
			query = query.replace("@@author_uuid@@", str(author.uuid))
		else:
			query = "SELECT id FROM rules WHERE room_name = '@@room_name@@' @@__EXCLUDED_RULE_ID__@@;"

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

		if includeGroupsRules:
			groupList = self.getGroups()



			for group in groupList:
				# Getting the rules expressed directly into this group (inheritance)
				ruleList.extend(group.getRules())
				
				# If this is a cross room validation, getting the rules expressed into the other rooms into the same group		
				if group.crossRoomsValidation and not excludeCrossRoomValidationRules:
					for groupRoom in group.getRooms():
						groupRoomRuleList = groupRoom.getRules()
						for groupRoomRule in groupRoomRuleList:
							if groupRoomRule.category in group.crossRoomsValidationCategories:
								if groupRoomRule.buildingName != self.buildingName or groupRoomRule.roomName != self.roomName:
									groupRoomRule.groupId = group.id
									ruleList.append(groupRoomRule)

		return ruleList


	def addRule(self, rule):

		rule.roomName = self.roomName
		rule.buildingName = self.buildingName
		rule.store()

		return rule

	def deleteRule(self, rule):
		rule.delete()

	def addUser(self, user):
		self.isClassInitialized()

		database = Database()
		database.open()

		query = "INSERT INTO users_rooms (room_name, building_name, user_uuid) VALUES ('@@room_name@@', '@@building_name@@', '@@user_uuid@@');"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@user_uuid@@", str(user.uuid))
		database.executeWriteQuery(query)

		database.close()
		

	def deleteUser(self, user):

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "DELETE FROM users_rooms WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@' AND user_uuid = '@@user_uuid@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@user_uuid@@", str(user.uuid))
		database.executeWriteQuery(query)

		database.close()

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.roomName 		!= None	: 	queryTemplate = queryTemplate.replace("@@room_name@@", self.roomName)
		if self.buildingName	!= None	: 	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.description		!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate


	def store(self):

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "SELECT COUNT(room_name) FROM rooms WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE rooms SET description = '@@description@@' WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		else:
			query = "INSERT INTO rooms (room_name, building_name, description) VALUES ('@@room_name@@', '@@building_name@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "SELECT * FROM rooms WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.roomName = queryResult[0][0]
			self.buildingName = queryResult[0][1]
			self.description = queryResult[0][2]
		else:
			database.close()
			raise Exception("Impossibile to find any room with the provided values")

		database.close()


	def delete(self):

		print "TODO: Consistency check not performed into table users_rooms"

		self.isClassInitialized()

		database = Database()
		database.open()

		query = "DELETE FROM rooms WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()


	def isClassInitialized(self):
		if not(self.roomName and self.buildingName):
			raise Exception("Room name and building name not specified")			

	def getDict(self):
		
		response = {}

		response["roomName"] = self.roomName
		response["buildingName"] = self.buildingName
		response["description"] = self.description

		return response	


	def __str__(self):
		return "Room " + str(json.dumps(self.getDict(), separators=(',',':')))

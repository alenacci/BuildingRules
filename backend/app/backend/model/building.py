import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Building:
	def __init__(self, buildingName = None, label = None, description = None):

			self.buildingName = buildingName
			self.label = label
			self.description = description

	def getBuilding(self):
		print "TODO: non yet implemented"

	def getRooms(self):

		print "TODO: non yet tested"

		from app.backend.model.room import Room
		
		query = "SELECT room_name FROM rooms WHERE building_name = '@@building_name@@';"

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		roomList = []
		for roomRecord in queryResult:
			room = Room(roomName = roomRecord[0], buildingName = self.buildingName)
			room.retrieve()
			roomList.append(room)

		return roomList

	def getGroups(self):
		print "TODO: non yet tested"

		from app.backend.model.group import Group
		
		query = "SELECT id FROM groups WHERE building_name = '@@building_name@@';"

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		groupList = []
		for groupRecord in queryResult:
			group = Group(id = groupRecord[0], buildingName = self.buildingName)
			group.retrieve()
			groupList.append(group)

		return groupList


	def getRules(self):		
		print "TODO: non yet implemented"

	def addRoom(self, room):
		room.buildingName = self.buildingName
		room.store()
		return room

	def addGroup(self, group):
		group.buildingName = self.buildingName
		group.store()
		return group

	def deleteRoom(self, room):
		room.delete()

	def deleteGroup(self, group):
		group.delete()

	def checkUserBinding(self, user):

		database = Database()

		query = "SELECT user_uuid FROM users_rooms WHERE building_name = '@@building_name@@' and user_uuid = '@@user_uuid@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace('@@user_uuid@@', str(user.uuid))
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		if len(queryResult) == 0:
			raise UserBuildingBindingError("The user is not associated with the requested building")


	def __replaceSqlQueryToken(self, queryTemplate):
		if self.buildingName 	!= None	: 	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.label			!= None	: 	queryTemplate = queryTemplate.replace("@@label@@", self.label)
		if self.description 	!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):
		database = Database()
		database.open()

		query = "SELECT COUNT(building_name) FROM buildings WHERE building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE buildings SET label = '@@label@@', description = '@@description@@' WHERE building_name = '@@building_name@@';"
		else:
			query = "INSERT INTO buildings (building_name, label, description) VALUES ('@@building_name@@', '@@label@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):
		database = Database()
		database.open()

		query = "SELECT * FROM buildings WHERE building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.buildingName = queryResult[0][0]
			self.label = queryResult[0][1]
			self.description = queryResult[0][2]
		else:
			database.close()
			raise BuildingNotFoundError("Impossibile to find any building with the provided values")

		database.close()


	def delete(self):
		print "TODO: Consistency check not performed - class Building"

		database = Database()
		database.open()

		query = "DELETE FROM buildings WHERE building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()


	def getDict(self):
		
		response = {}

		response["buildingName"] = self.buildingName
		response["label"] = self.label
		response["description"] = self.description

		return response	


	def __str__(self):
		return "Building: " + str(self.buildingName) + " - " + str(self.label) + " - " + str(self.description)
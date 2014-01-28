import json
from app.backend.commons.errors import *
from app.backend.model.building import Building

class BuildingsManager:
	def __init__(self):
		pass

	def getInfo(self, buildingName):
	
		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.getDict()

	def checkUserBinding(self, buildingName, username):

		from app.backend.model.user import User

		building = Building(buildingName = buildingName)
		building.retrieve()

		user = User(username = username)
		user.retrieve()

		building.checkUserBinding(user)

	def getGroups(self, buildingName):
		building = Building(buildingName = buildingName)
		building.retrieve()

		groupList = []
		for group in building.getGroups():
			groupList.append(group.getDict())

		return {"groups" : groupList}


	def getRooms(self, buildingName):
		building = Building(buildingName = buildingName)
		building.retrieve()

		roomList = []
		for room in building.getRooms():
			roomList.append(room.getDict())

		return {"rooms" : roomList}

	def addRoom(self, roomName, buildingName, description):
		
		from app.backend.model.room import Room
		room = Room(roomName = roomName,  buildingName = buildingName, description = description)

		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.addRoom(room).getDict()
		
	def addGroup(self, buildingName, description, crossRoomsValidation, crossRoomsValidationCategories):
		return self.__addOrModifyGroup(buildingName = buildingName, description =description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories)


	def editGroup(self, groupId, buildingName, description, crossRoomsValidation, crossRoomsValidationCategories):
		return self.__addOrModifyGroup(buildingName = buildingName, description =description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories, groupId = groupId)

	def __addOrModifyGroup(self, buildingName, description, crossRoomsValidation, crossRoomsValidationCategories, groupId = None):



		if type(crossRoomsValidation) == int:
			crossRoomsValidation = bool(crossRoomsValidation)
		elif type(crossRoomsValidation) == str or type(crossRoomsValidation) == unicode:

			if str(crossRoomsValidation.upper()) == "TRUE" or str(crossRoomsValidation.upper()) == "1":
				crossRoomsValidation = True
			else:
				crossRoomsValidation = False

		elif type(crossRoomsValidation) != bool:
			raise IncorrectInputDataTypeError("crossRoomsValidation must be a booelan value (True,False) or integer value (1,0)")


		if not crossRoomsValidation:
			crossRoomsValidationCategories = []
		else:
			crossRoomsValidationCategories = json.loads(crossRoomsValidationCategories)


		if crossRoomsValidation and len(crossRoomsValidationCategories) == 0:
			raise MissingInputDataError("Selecting crossRoomsValidation you need to insert at least one rule category in crossRoomsValidationCategories")

		from app.backend.model.group import Group
		group = Group(id = groupId, buildingName = buildingName, description = description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories)

		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.addGroup(group).getDict()


	def __str__(self):
		return "BuildingsManager: "
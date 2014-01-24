import json
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
		
	def addGroup(self, buildingName, description):
		from app.backend.model.group import Group
		group = Group(buildingName = buildingName, description = description)

		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.addGroup(group).getDict()

	def __str__(self):
		return "BuildingsManager: "
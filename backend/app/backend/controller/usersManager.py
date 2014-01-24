import json
from app.backend.commons.errors import *
from app.backend.model.user import User


class UsersManager:
	def __init__(self):
		pass

	def getUser(self, username, password = None):
		
		user = User(username = username, password = password)		
		user.retrieve()
		return user

	def getInfo(self, username):
		user = User(username = username)		
		user.retrieve()

		return user.getDict()
		

	def register(self, creatorUuid, newUserUsername, newUserPassword, newUserEmail, newUserPersonName, newUserLevel):

		creatorUser = User(uuid = creatorUuid)		
		creatorUser.retrieve()

		if creatorUser.level != 0:
			raise UserCredentialError("Only root user can create new users")

		try:
			user = User(username = newUserUsername)
			user.retrieve()
			raise UsernameNotAvailableError("The username " + newUserUsername + " has been alredy assigned")

		except UserNotFoundError as e:
		
			if not(newUserUsername and newUserPassword and newUserEmail and newUserPersonName and newUserLevel):
				raise MissingInputDataError("Some input data are missing to register a new user")

			user = User(username = newUserUsername, password = newUserPassword, email = newUserEmail, personName = newUserPersonName, level = newUserLevel)
			user.store()

			return user.getDict()


	def getBuildingList(self, username):
		user = User(username = username)		
		user.retrieve()

		response = []
		buildingList = user.getBuildings()
		for building in buildingList:
			response.append(building.getDict())
			

		return {"buildings" : response}

	def getRoomList(self, username):
		print "TODO: not yet implemented"

	def addRoom(self, username):
		print "TODO: not yet implemented"

	def __str__(self):
		return "UserManager: "
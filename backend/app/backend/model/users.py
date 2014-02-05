import sys
import json
from app.backend.commons.errors import *
from app.backend.commons.database import Database
from app.backend.model.user import User

class Users:
	def __init__(self):
		pass

	def getAllUsers(self):

		userList = []

		database = Database()
		query = "SELECT * FROM users;"
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		for record in queryResult:
			uuid = record[0]
			username = record[1]
			email = record[2]
			password = record[3]
			personName = record[4]
			level = record[5]

			user = User(uuid = uuid, username = username, email = email, password = password, personName = personName, level = level)

			userList.append(user)

		
		return userList

	def __str__(self):
		return "Users: "
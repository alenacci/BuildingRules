import sys
import json
from app.backend.commons.errors import *
from app.backend.commons.inputDataChecker import checkData
from app.backend.model.user import User
from app.backend.model.users import Users
from app.backend.model.rules import Rules
from app.backend.model.mturk import Mturk
import time
import datetime

class MTurkManager:
	def __init__(self):
		pass

	def _getTokenFromDb(self, userUuid, day):
		mturk = Mturk(userUuid = userUuid, day = day)
		mturk.retrieve()
		return mturk.token

	def getTodayToken(self, userUuid):

		days = ['2014-02-13','2014-02-14','2014-02-15','2014-02-16','2014-02-17','2014-02-18','2014-02-19']
		today = str(time.strftime("%Y-%m-%d"))

		if today not in days:
			raise UnknownError("Today is not enabled for to use by the MTurk service. All the actions performed today will not be paid!")
		
		day = days.index(today)

		user = User(uuid = userUuid)
		user.retrieve()

		userRules = user.getCreatedRules()

		createdRulesCount = 0
		editedRulesCount = 0

		for rule in userRules:
			if str(rule.creationTimestamp).startswith(today): createdRulesCount += 1
			elif str(rule.lastEditTimestamp).startswith(today): editedRulesCount += 1

		userActionsCount = createdRulesCount + editedRulesCount

		result = {}

		requiredUserActions = [10, 8, 7, 5 , 4, 3, 2]
		
		if userActionsCount >= requiredUserActions[day]:
			result["message"] = "You completed your today task!"
			result["token"] = self._getTokenFromDb(userUuid = userUuid, day = day)
		else:
			result["message"] = "You have still to perform " + str(requiredUserActions[day] - userActionsCount) + " actions on the rule sets!"

		return result

		

	def __str__(self):
		return "MTurkManager: "
import json
from app.backend.commons.errors import *
from app.backend.model.group import Group

class GroupsManager:
	def __init__(self):
		pass

	def getInfo(self, groupId, buildingName):
		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()
		return group.getDict()


	def getRules(self, groupId, buildingName):
		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		ruleList = group.getRules()

		response = []
		for rule in ruleList:
			response.append(rule.getDict())
			
		return {"rules" : response}


	def getRooms(self, groupId, buildingName):
		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		roomList = []
		for room in group.getRooms():
			roomList.append(room.getDict())

		return {"rooms" : roomList}		

	def addRoom(self, groupId, roomName, buildingName):
		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		from app.backend.model.room import Room
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()


		if group.crossRoomsValidation:
			print "TODO This part of the method as not been tested"
			# In this case we have to check that the room doesn't belong to another CrossRoomValidatioGroup
			from app.backend.model.building import Building
			building = Building(buildingName = buildingName)
			building.retrive()
			crvgList = building.getCrossRoomValidationGroups(roomName = roomName, validationCategories = group.crossRoomsValidationCategories)

			if len(crvgList) > 0:
				raise WrongBuildingGroupRipartitionError("A room can belong to only one cross validation group per category. Room " + roomName + " in already in group " + crvgList[0])

		group.addRoom(room)

		return room.getDict()

	def addRule(self, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None):
		return self.__addOrModifyRule(priority = priority, buildingName = buildingName, groupId = groupId,  authorUuid = authorUuid, ruleBody = ruleBody)

	def editRule(self, ruleId = None, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None):

		from app.backend.model.rule import Rule
		oldRule = Rule(id = ruleId)
		oldRule.retrieve()

		from app.backend.model.user import User
		author = User(uuid = authorUuid)
		author.retrieve()

		result = self.__addOrModifyRule(ruleId = ruleId, priority = priority, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, ruleBody = ruleBody)

		from app.backend.controller.notificationsManager import NotificationsManager
		notifications = NotificationsManager()
		messageSubject = "Rule modified in building " + str(buildingName) + " group " + str(groupId)
		messageText = "The user " + str(author.username) + " edited (or tried to edit) the rule <<" + str(oldRule.getFullRepresentation()) + ">>. The new rule is <<" + str(ruleBody) + ">>"
		notifications.sendNotification(buildingName = buildingName, groupId = groupId, messageSubject = messageSubject, messageText = messageText) 

		return result
		

	def deleteRule(self, ruleId, buildingName, groupId):
		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId)
		rule.retrieve()

		group.deleteRule(rule)

		return {}

	def getRuleInfo(self, buildingName = None, groupId = None, ruleId = None):
		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId, buildingName = buildingName, groupId = groupId)
		rule.retrieve()

		return rule.getDict()


	def __addOrModifyRule(self, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None, ruleId = None):

		try:
			antecedent = ruleBody.split("then")[0].replace("if ", "").strip()
			consequent = ruleBody.split("then")[1].strip()
		except Exception as e:
			raise NotWellFormedRuleError("There is a syntax error in the rule you are trying to save")

		from app.backend.controller.actionManager import ActionManager
		actionManager = ActionManager()
		category = actionManager.getAction(consequent).category

		if int(str(priority)) < 0 or int(str(priority)) > 200:
			raise RulePriorityError("Rules for groups must have a priority value between 0 and 200. You inserted " + str(priority))


		
		from app.backend.model.rule import Rule
		from app.backend.model.group import Group

		if not ruleId:
			rule = Rule(priority = priority, category = category, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, antecedent = antecedent, consequent = consequent, enabled = True)
		else:
			rule = Rule(id = ruleId)
			rule.retrieve()
			author = rule.getAuthor()

			
			rule.antecedent = antecedent
			rule.consequent = consequent
			rule.authorUuid = authorUuid

			editor = rule.getAuthor()

			if author.level > editor.level:
				raise UserCredentialError("The rule you want to edit was created by an higher level user.")

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		if not ruleId and not rule.checkIfUnique():
			raise DuplicatedRuleError("The submitted rule is already been saved for the considered group.")

		# excludedRuleId is needed to ignore the rule that the user want to edit
		excludedRuleId = ruleId if ruleId else None		


		ruleCheckErrorList = []
		groupRoomList = group.getRooms()
		for room in groupRoomList:

			temporaryRuleSet = []
			temporaryRuleSet.extend(room.getRules(author = False, includeGroupsRules = True, excludedRuleId = False, excludeCrossRoomValidationRules = True))
			temporaryRuleSet.extend(group.getRules(excludedRuleId = excludedRuleId))
			temporaryRuleSet.append(rule)

			for i in range(0, len(temporaryRuleSet)):
				temporaryRuleSet[i].groupId = None
			

			from app.backend.controller.rulesetChecker import RulesetChecker
			rulesetChecker = RulesetChecker(temporaryRuleSet)

			ruleCheckErrorList.extend(rulesetChecker.check())

		if len(ruleCheckErrorList) == 0:
			if ruleId: 
				rule.id = ruleId
				rule.setPriority(priority)


			return group.addRule(rule).getDict()
		else:
			raise RuleValidationError(ruleCheckErrorList)

	def __str__(self):
		return "GroupsManager: "
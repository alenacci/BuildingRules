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

		group.addRoom(room)

		return room.getDict()

	def addRule(self, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None):
		return self.__addOrModifyRule(priority = priority, buildingName = buildingName, groupId = groupId,  authorUuid = authorUuid, ruleBody = ruleBody)

	def editRule(self, ruleId = None, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None):
		return self.__addOrModifyRule(ruleId = ruleId, priority = priority, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, ruleBody = ruleBody)

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

		print "TODO Category automatic detection "
		category = "UNKW"
		
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
			temporaryRuleSet.extend(room.getRules(author = False, includeGroupsRules = False, excludedRuleId = False))
			temporaryRuleSet.extend(group.getRules(excludedRuleId = excludedRuleId))
			temporaryRuleSet.append(rule)

			for i in range(0, len(temporaryRuleSet)):
				temporaryRuleSet[i].groupId = None
				temporaryRuleSet[i].roomName = "100"	#Fake room name

			

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
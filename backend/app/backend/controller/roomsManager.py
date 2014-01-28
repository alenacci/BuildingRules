import json
from app.backend.commons.errors import *
from app.backend.model.room import Room


class RoomsManager:
	def __init__(self):
		pass

	def getInfo(self, roomName, buildingName):
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()
		return room.getDict()

	def getRules(self, roomName, buildingName, username = None, includeGroupsRules = False):
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		ruleList = []

		if username:
			from app.backend.model.user import User
			user = User(username = username)
			user.retrieve()
			ruleList = room.getRules( author = user, includeGroupsRules = includeGroupsRules)
		else:
			ruleList = room.getRules( includeGroupsRules = includeGroupsRules )

		response = []
		for rule in ruleList:
			response.append(rule.getDict(buildingName = buildingName, roomName = roomName))
			

		return {"rules" : response}


	def getTriggers(self, roomName, buildingName):
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		triggerList = room.getTriggers( )

		response = []
		for trigger in triggerList:
			response.append(trigger.getDict())
			

		return {"triggers" : response}

	def getActions(self, roomName, buildingName):
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		actionList = room.getActions( )

		response = []
		for action in actionList:
			response.append(action.getDict())
			

		return {"actions" : response}

	def bindTrigger(self):
		print "TODO: not yet implemented"

	def bindAction(self):
		print "TODO: not yet implemented"

	def deleteRule(self, ruleId, buildingName, roomName):
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId)
		rule.retrieve()

		room.deleteRule(rule)

		return {}

	def getRuleInfo(self, buildingName = None, roomName = None, ruleId = None):
		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId, buildingName = buildingName, roomName = roomName)
		rule.retrieve()

		return rule.getDict(buildingName = None, roomName = None)


	def setRulePriority(self, buildingName, roomName, ruleId, rulePriority):

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId, buildingName = buildingName, roomName = roomName)
		rule.retrieve()
		rule.setPriority(buildingName = buildingName, roomName = roomName, priority = rulePriority)

		return rule.getDict(buildingName = buildingName, roomName = roomName)


	def addRule(self, priority, buildingName, roomName, authorUuid, ruleBody):
		return self.__addOrModifyRule(priority = priority, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, ruleBody = ruleBody)

	def editRule(self, ruleId, priority, buildingName, roomName, authorUuid, ruleBody):
		return self.__addOrModifyRule(ruleId = ruleId, priority = priority, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, ruleBody = ruleBody)		

	def __addOrModifyRule(self, priority = None, buildingName = None, roomName = None, authorUuid = None, ruleBody = None, ruleId = None):

		try:
			antecedent = ruleBody.split("then")[0].replace("if ", "").strip()
			consequent = ruleBody.split("then")[1].strip()
		except Exception as e:
			raise NotWellFormedRuleError("There is a syntax error in the rule you are trying to save")

		print "TODO Category automatic detection "
		category = "UNKW"
		
		from app.backend.model.rule import Rule
		from app.backend.model.room import Room

		if not ruleId:
			rule = Rule(priority = priority, category = category, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, antecedent = antecedent, consequent = consequent, enabled = True)
		else:
			rule = Rule(id = ruleId)
			rule.retrieve()
			author = rule.getAuthor()

			
			rule.antecedent = antecedent
			rule.consequent = consequent
			rule.authorUuid = authorUuid
			rule.authorUuid = authorUuid			

			editor = rule.getAuthor()

			if author.level > editor.level:
				raise UserCredentialError("The rule you want to edit was created by an higher level user.")

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		if not ruleId and not rule.checkIfUnique():
			raise DuplicatedRuleError("The submitted rule is already been saved for the considered room.")

		# excludedRuleId is needed to ignore the rule that the user want to edit
		excludedRuleId = ruleId if ruleId else None		

		temporaryRuleSet = []
		temporaryRuleSet.extend(room.getRules(author = False, includeGroupsRules = True, excludedRuleId = excludedRuleId))
		temporaryRuleSet.append(rule)


		for i in range(0, len(temporaryRuleSet)):
			temporaryRuleSet[i].groupId = None
			temporaryRuleSet[i].roomName = roomName


		from app.backend.controller.rulesetChecker import RulesetChecker
		rulesetChecker = RulesetChecker(temporaryRuleSet)

		ruleCheckErrorList = rulesetChecker.check()

		if len(ruleCheckErrorList) == 0:
			if ruleId: 
				rule.id = ruleId
				rule.setPriority(priority)
			return room.addRule(rule).getDict()
		else:
			raise RuleValidationError(ruleCheckErrorList)

	def __str__(self):
		return "RoomsManager: "
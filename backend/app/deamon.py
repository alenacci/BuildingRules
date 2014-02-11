import sys
import time
import datetime
import copy

from app.backend.commons.console import flash
from app.backend.commons.errors import *
from app.backend.controller.groupsManager import GroupsManager
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager

from app.backend.model.buildings import Buildings
from app.backend.model.rules import Rules

# REMEMBER
# After the rule partioning among pure rule and CRVG-rules, the attributes of the rule classes are changed in this way:
#
#	- For a pure room rule: rule.roomName = <roomName>  rule.groupId = None
#	- For a pure group rule: rule.roomName = <roomName>  rule.groupId = <groupId>
#	- For a CRVG rule: rule.roomName = <theOriginalRoomName>  rule.groupId = <groupId>
#


def checkRuleTrigger(rule):

	triggerManager = TriggerManager()
	trigger, originalModel, parameters = triggerManager.getTriggerAndTemplateAndParameterValues(rule.antecedent)
	
	parameters.update({'buildingName' : rule.buildingName})
	if rule.roomName: parameters.update({'roomName' : rule.roomName})
	if rule.groupId: parameters.update({'groupId' : rule.groupId})
	
	driver = triggerManager.getTriggerDriver(trigger, parameters)


	message = "Rule " + str(rule.id) + " (" + str(rule.buildingName)
	if rule.groupId: message += ".g[" + str(rule.groupId) + "]"
	if rule.roomName: message += ".r[" + str(rule.roomName) + "]"

	if driver.eventTriggered():
		flash(message + ") actuated; antecedent is '" + rule.antecedent + "'...", "green")
		return True
	else:
		flash(message + ") NOT actuated; antecedent is '" + rule.antecedent + "'...", "red")

	return False


def executeRule(rule):
	actionManager = ActionManager()
	action, originalModel, parameters = actionManager.getActionAndTemplateAndParameterValues(rule.consequent)

	parameters.update({'buildingName' : rule.buildingName})
	if rule.roomName: parameters.update({'roomName' : rule.roomName})
	if rule.groupId: parameters.update({'groupId' : rule.groupId})

	driver = actionManager.getActionDriver(action, parameters)

	message = "Rule " + str(rule.id) + " (" + str(rule.buildingName)
	if rule.groupId: message += ".g[" + str(rule.groupId) + "]"
	if rule.roomName: message += ".r[" + str(rule.roomName) + "]"


	flash(message + ") actuated; consequent is '" + rule.consequent + "'...")
	driver.actuate()

	rules = Rules()
	rules.setActiveRule(buildingName = rule.buildingName, roomName = rule.roomName, ruleId = rule.id)

def notifyIgnoredRule(rule):
	pass

def start():
	flash("BuildingRules Deamon is active...")
	while(1):
		try:
			main()
		except Exception as e:
			import logging
			logging.exception("")
			flash(e.message)

		time.sleep(600)
		
def main():

	print
	print
	print
	flash("Starting the actuation process...", "yellow")

	buildings = Buildings()
	buildingsManager = BuildingsManager()
	groupsManager = GroupsManager()
	rules = Rules()

	rules.resetActiveRules()
	
	for building in buildings.getAllBuildings():

		flash("Working on building '" + building.buildingName + "'...", "blue")

		triggeredRules = []
		triggeredRulesId = []
		
		# Getting all the triggered rules for the considered building	
		buildingRules = building.getRules()

		if len(buildingRules) == 0:
			flash("Nothing to do...")

		if len(buildingRules):
			for rule in buildingRules:

				if rule.roomName and not rule.groupId:

					if checkRuleTrigger(rule):
						# If the antecedent of the rule is triggered, let us store the rule as triggered!
						triggeredRules.append(rule)
						triggeredRulesId.append(rule.id)
				
				elif rule.groupId and not rule.roomName:

					groupRoomList = groupsManager.getRooms(buildingName = building.buildingName, groupId = rule.groupId)["rooms"]
					for room in groupRoomList:

						roomName = room["roomName"]
						newRule = copy.copy(rule)			# I need to copy the object to modify the room name
						newRule.roomName = roomName

						if checkRuleTrigger(newRule):
							# If the antecedent of the rule is triggered, let us store the rule as triggered!
							triggeredRules.append(newRule)
							triggeredRulesId.append(newRule.id)



			flash(building.buildingName + " - Total rules: " + str(len(buildingRules)), "gray")
			flash(building.buildingName + " - Triggered rules: " + str(len(triggeredRules)), "gray")


			# Now, let us partition rules among "Pure-Room-Rules" and "CRVG-Rules"
			roomScheduledRules = {}
			crvgScheduledRules = {}

			for rule in triggeredRules:



				if rule.roomName:

					# In this case we are selecting the rules spiecified for a specific room.
					# If the rule (for a specific category) is saved into a room belonging to a CRVG, I have to save it into the crvgScheduledRules set.
					# If the rule is not part of CRVG ruleset, then it is savet into the roomScheduledRules set.

					buildingName = building.buildingName
					roomName = rule.roomName
					validationCategories = [rule.category]
					crvgList = buildingsManager.getCrossRoomValidationGroups(buildingName = buildingName, roomName = roomName, validationCategories = validationCategories)

					if len(crvgList) == 0:


						if not roomName in roomScheduledRules.keys():
							roomScheduledRules[roomName] = []

						roomScheduledRules[roomName].append(rule)

					elif len(crvgList) == 1:

						
						if not crvgList[0].id in crvgScheduledRules.keys():
							crvgScheduledRules[crvgList[0].id] = []
						
						rule.gropuId = crvgList[0].id
						crvgScheduledRules[crvgList[0].id].append(rule)

					else:
						raise WrongBuildingGroupRipartitionError(roomName + " has been found to be part of two different Cross Room Validation Groups. This is not allowed.")

				elif rule.groupId and not rule.roomName:


					# Here we are selecting those rules that have been specified of a specific group.
					# Those groups can be standard groups or CRV GROUPS on a specific category. In the first case, i have to add a copy of the rule in each of the group rooms.
					# In the second case I have to add the rule to the corresponding CRVG dict (if the rule category is right).

					if groupsManager.isCrossRoomsValidationGroup(buildingName = building.buildingName, groupId = rule.groupId, crossRoomsValidationCategory = rule.category):

						if not rule.groupId in crvgScheduledRules.keys():
							crvgScheduledRules[rule.groupId] = []
						
						crvgScheduledRules[rule.groupId].append(rule)

					else:		
						raise UnknownError("Unexpected error into the database.")




				else:
					raise UnknownError("The rule with id " + rule.id + " has both the groupId and roomName field not null.")

			flash(building.buildingName + " - Number of rooms: " + str(len(roomScheduledRules.keys())), "gray")
			flash(building.buildingName + " - Number of CRV Groups: " + str(len(crvgScheduledRules.keys())), "gray")

			flash("Executing actions for rooms...", "yellow")
			# Executing the rules per each room
			# In the case I have the same action category, I'll take the action with higher priority
			for roomName in roomScheduledRules.keys():
				flash("Room [" + building.buildingName + "." + roomName + "]..." , "blue")				
				ruleList = roomScheduledRules[roomName]
				#Let us order by rule priority
				ruleList = sorted(ruleList, key=lambda rule: rule.getPriority(), reverse=True)

				alreadyAppliedCategories = []
				for rule in ruleList:
					
					if rule.category not in alreadyAppliedCategories:
						alreadyAppliedCategories.append(rule.category)
						executeRule(rule)
					else:
						flash(building.buildingName + " - Room " + roomName + ", ruleId " + str(rule.id) + " ignored.")

			flash("Executing actions for CRV Groups...", "yellow")
			for crvgId in crvgScheduledRules.keys():
				flash("Group " + building.buildingName + ".g[" + str(crvgId) + "]..." , "blue")				
				ruleList = crvgScheduledRules[crvgId]

				#Let us order by rule priority
				ruleList = sorted(ruleList, key=lambda rule: rule.getPriority(), reverse=True)

				alreadyAppliedCategories = []
				for rule in ruleList:
					if rule.category not in alreadyAppliedCategories:
						alreadyAppliedCategories.append(rule.category)
						executeRule(rule)
					else:
						flash(building.buildingName + " - CRVGroup " + str(crvgId) + ", ruleId " + str(rule.id) + " ignored.")
						notifyIgnoredRule(rule)

	flash("The actuation process is ended.", "yellow")

import sys
import time
import datetime

from app.backend.commons.errors import *
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.triggerManager import TriggerManager

from app.backend.model.buildings import Buildings

# REMEMBER
# After the rule partioning among pure rule and CRVG-rules, the attributes of the rule classes are changed in this way:
#
#	- For a pure room rule: rule.roomName = <roomName>  rule.groupId = None
#	- For a pure group rule: rule.roomName = <roomName>  rule.groupId = <groupId>
#	- For a CRVG rule: rule.roomName = <theOriginalRoomName>  rule.groupId = <groupId>
#


def checkRuleTrigger(rule):
	triggerManager = TriggerManager()
	trigger, originalModel, parameterValues = triggerManager.getTriggerAndTemplateAndParameterValues(rule.antecedent)
	driver = triggerManager.getTriggerDriver(trigger, parameterValues)

	return driver.eventTriggered()


def executeRule(rule):
	pass

def notifyIgnoredRule(rule):
	pass

def start():
	flash("BuildingRules Deamon is active...")
	while(1):
		main()
		time.sleep(30)
		
def flash(message):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print st + " > " + message 

def main():

	buildings = Buildings()
	
	
	for building in buildings.getAllBuildings():

		flash("Running actions for building '" + building.buildingName + "'...")

		triggeredRules = []
		triggeredRulesId = []
		
		# Getting all the triggered rules for the considered building	
		buildingRules = building.getRules()
		for rule in buildingRules:

			if rule.id not in triggeredRulesId and checkRuleTrigger(rule):
				# If the antecedent of the rule is triggered, let us store the rule as triggered!
				triggeredRules.append(rule)
				triggeredRulesId.append(rule.id)


		flash(building.buildingName + " - Total rules: " + str(len(buildingRules)))
		flash(building.buildingName + " - Triggered rules: " + str(len(triggeredRules)))


		# Now, let us partition rules among "Pure-Room-Rules" and "CRVG-Rules"
		roomScheduledRules = {}
		crvgScheduledRules = {}

		for rule in triggeredRules:

			if rule.roomName and not rule.groupId:
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
					raise WrongBuildingGroupRipartition(roomName + " has been found to be part of two different Cross Room Validation Groups. This is not allowed.")

			elif rule.groupId and not rule.roomName:
				# Here we are selecting those rules that have been specified of a specific group.
				# In this case, this rules has to be copied inside each room roomScheduledRules set.

				groupRoomList = groupsManager.getRooms(buildingName = building.name, groupId = rule.groupId)["rooms"]

				for room in groupRoomList:
					roomName = room["roomName"]
					rule.roomName = roomName
					roomScheduledRules[roomName].append(rule)

			else:
				raise UnknownError("The rule with id " + rule.id + " has both the groupId and roomName field not null.")


		flash(building.buildingName + " - Number of rooms: " + str(len(roomScheduledRules.keys())))
		flash(building.buildingName + " - Number of CRV Groups: " + str(len(crvgScheduledRules.keys())))

		# Executing the rules per each room
		# In the case I have the same action category, I'll take the action with higher priority
		for roomName in roomScheduledRules.keys():
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

		for crvgId in crvgScheduledRules.keys():
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

		flash("The actuation process is ended.")

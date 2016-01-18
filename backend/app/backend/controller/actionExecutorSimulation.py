__author__ = 'jacopo'
# ###########################################################
#
# BuildingRules Project
# Politecnico di Milano
# Author: Alessandro A. Nacci
#
# This code is confidential
# Milan, March 2014
#
############################################################
import os

import sys
import time
import datetime
import copy
from flask import json

from app.backend.commons.console import flash
from app.backend.commons.errors import *
from app.backend.controller.groupsManager import GroupsManager
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager

from app.backend.model.buildings import Buildings
from app.backend.model.rules import Rules


class ActionExecutorSimulation:
    def __init__(self, simulationParameters=None, roomFilter=None):

        # simulationParameters is a dictionary; here an example
        #		simulationParameters = {}
        # 		simulationParameters['roomTemperature'] = "75F"
        # 		simulationParameters['occupancy'] = True
        # 		simulationParameters['day'] = "Monday"
        # 		simulationParameters['date'] = "25/04"
        # 		simulationParameters['weather'] = "Sunny"
        # 		simulationParameters['externalTemperature'] = "75F"
        # 		simulationParameters['time'] = "16:00"	--> USE 24 HOURS!!! NOT AM/PM
        # 		simulationParameters['resultsBufferFile'] = "logfile.txt"

        # roomFilter is a list of dicionaries containes the list of rooms you want to consider; here an example
        #
        #		roomFilter = []
        #		roomFilter[0] = {'buildingName' : 'CSE', 'roomName' : '300'}
        #		roomFilter[1] = {'buildingName' : 'EEE', 'roomName' : '350'}
        #		roomFilter[2] = {'buildingName' : 'CSE', 'roomName' : '220'}

        self.simulationParameters = simulationParameters
        self.roomFilter = roomFilter

    def skipRuleOnRoomFilter(self, buildingName, roomName):

        if not self.roomFilter:    return False

        for room in self.roomFilter:
            if (room["buildingName"] == buildingName) and (room["roomName"] == roomName):
                return False

        return True


    def checkRuleTrigger(self, rule):

        ### TRIGGER RETURN VALUES ###
        #set it as an empty set
        rule.triggers_returned_values = {}

        triggerManager = TriggerManager()
        #trigger, originalModel, parameters = triggerManager.getTriggerAndTemplateAndParameterValues(rule.antecedent)
        translatedTriggers = triggerManager.translateTrigger(rule.antecedent)

        message = "Rule " + str(rule.id) + " (" + str(rule.buildingName)

        #flash(message + ") checking the '" + rule.antecedent + "'...", "gray")
        for triggerInfo in translatedTriggers["triggers"]:

            trigger = triggerInfo["trigger"]
            parameters = triggerInfo["parameterValues"]

            parameters.update({'buildingName': rule.buildingName})
            if rule.roomName: parameters.update({'roomName': rule.roomName})
            if rule.groupId: parameters.update({'groupId': rule.groupId})
            if self.simulationParameters:
                localSimulationParameters = self.simulationParameters.copy()
                localSimulationParameters.update({'ruleId': rule.id, 'ruleText': rule.getFullRepresentation()})
                parameters.update({'simulationParameters': localSimulationParameters})

            driver = triggerManager.getTriggerDriver(trigger, parameters)

            if rule.groupId: message += ".g[" + str(rule.groupId) + "]"
            if rule.roomName: message += ".r[" + str(rule.roomName) + "]"

            try:
                if driver.eventTriggered():
                    ### RETURN VALUES ###
                    if driver.parameters.has_key('returnValues'):
                        rule.triggers_returned_values = dict(driver.parameters['returnValues'].items() +
                                                             rule.triggers_returned_values.items())

                    #flash(message + ") the antecedent portion '" + trigger.ruleAntecedent + "' is TRUE...", "green")
                else:
                    #flash(message + ") the antecedent portion '" + trigger.ruleAntecedent + "' is FALSE...", "red")
                    #flash(message + ") NOT ACTUATED - the antecedent '" + rule.antecedent + "' is FALSE...", "red")
                    return False
            except Exception as e:
                #flash(message + ") error while reading the trigger! " + str(e), 'red')
                return False

        #flash(message + ") ACTUATED the antecedent '" + rule.antecedent + "' is TRUE...", "green")
        return True


    def executeRule(self, rule):
        actionManager = ActionManager()
        action, originalModel, parameters = actionManager.getActionAndTemplateAndParameterValues(rule.consequent)

        parameters.update({'buildingName': rule.buildingName})
        if rule.roomName: parameters.update({'roomName': rule.roomName})
        if rule.groupId: parameters.update({'groupId': rule.groupId})
        if self.simulationParameters:
            localSimulationParameters = self.simulationParameters.copy()
            localSimulationParameters.update({'ruleId': rule.id, 'ruleText': rule.getFullRepresentation()})
            parameters.update({'simulationParameters': localSimulationParameters})

        ### TRIGGER RETURN VALUES
        parameters.update({'triggerReturnedValues': rule.triggers_returned_values})

        driver = actionManager.getActionDriver(action, parameters)

        message = "Rule " + str(rule.id) + " (" + str(rule.buildingName)
        if rule.groupId: message += ".g[" + str(rule.groupId) + "]"
        if rule.roomName: message += ".r[" + str(rule.roomName) + "]"

        #flash(message + ") actuated; consequent is '" + rule.consequent + "'...")
        try:
            driver.actuate()
        except Exception as e:
            flash(message + ") Erro while actuating the consequent '" + rule.consequent + "'... " + str(e), 'red')

        #TODO: remove comment after GAME
        if not self.simulationParameters:
            now = datetime.datetime.now()
            hour = int(now.hour)
            rules = Rules()
            if int(self.simulationParameters["time"][:2]) == hour:
                rules.setActiveRule(buildingName=rule.buildingName, roomName=rule.roomName, ruleId=rule.id)

    def notifyIgnoredRule(self, rule):
        pass

    def start(self, only_real_time_triggers=False):

        import time, datetime

        startTimeMilliseconds = long((time.time() + 0.5) * 1000)

        analyzedRoomCounter = 0

        #flash("Starting the actuation process...", "yellow")

        buildings = Buildings()
        buildingsManager = BuildingsManager()
        groupsManager = GroupsManager()
        rules = Rules()

        rules.resetActiveRules()

        for building in buildings.getAllBuildings():

            #flash("Working on buildings '" + building.buildingName + "'...", "blue")

            triggeredRules = []
            triggeredRulesId = []

            # Getting all the triggered rules for the considered buildings
            buildingRules = building.getRules()

            #if len(buildingRules) == 0:
                #flash("Nothing to do...")

            if len(buildingRules):
                for rule in buildingRules:

                    ### REAL TIME FILTERING ###
                    if only_real_time_triggers:
                        if not rule.hasRealTimeAntecedent():
                            continue
                        #else:
                            #flash("rule with realtime antecedent " + str(rule.id), "blue")


                    if rule.roomName and not rule.groupId:

                        if self.skipRuleOnRoomFilter(buildingName=building.buildingName,
                                                     roomName=rule.roomName): continue
                        analyzedRoomCounter += 1

                        if self.checkRuleTrigger(rule):
                            # If the antecedent of the rule is triggered, let us store the rule as triggered!
                            triggeredRules.append(rule)
                            triggeredRulesId.append(rule.id)

                    elif rule.groupId and not rule.roomName:

                        groupRoomList = \
                            groupsManager.getRooms(buildingName=building.buildingName, groupId=rule.groupId)["rooms"]
                        for room in groupRoomList:

                            if self.skipRuleOnRoomFilter(buildingName=building.buildingName,
                                                         roomName=room.roomName): continue

                            roomName = room["roomName"]
                            newRule = copy.copy(rule)  # I need to copy the object to modify the room name
                            newRule.roomName = roomName

                            if self.checkRuleTrigger(newRule):
                                # If the antecedent of the rule is triggered, let us store the rule as triggered!
                                triggeredRules.append(newRule)
                                triggeredRulesId.append(newRule.id)

                #flash(building.buildingName + " - Total rules: " + str(len(buildingRules)), "gray")
                #flash(building.buildingName + " - Triggered rules: " + str(len(triggeredRules)), "gray")


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
                        crvgList = buildingsManager.getCrossRoomValidationGroups(buildingName=buildingName,
                                                                                 roomName=roomName,
                                                                                 validationCategories=validationCategories)

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
                            raise WrongBuildingGroupRipartitionError(
                                roomName + " has been found to be part of two different Cross Room Validation Groups. This is not allowed.")

                    elif rule.groupId and not rule.roomName:


                        # Here we are selecting those rules that have been specified of a specific group.
                        # Those groups can be standard groups or CRV GROUPS on a specific category. In the first case, i have to add a copy of the rule in each of the group rooms.
                        # In the second case I have to add the rule to the corresponding CRVG dict (if the rule category is right).

                        if groupsManager.isCrossRoomsValidationGroup(buildingName=building.buildingName,
                                                                     groupId=rule.groupId,
                                                                     crossRoomsValidationCategory=rule.category):

                            if not rule.groupId in crvgScheduledRules.keys():
                                crvgScheduledRules[rule.groupId] = []

                            crvgScheduledRules[rule.groupId].append(rule)

                        else:
                            raise UnknownError("Unexpected error into the database.")




                    else:
                        raise UnknownError(
                            "The rule with id " + rule.id + " has both the groupId and roomName field not null.")

                #flash(building.buildingName + " - Number of rooms: " + str(len(roomScheduledRules.keys())), "gray")
                #flash(building.buildingName + " - Number of CRV Groups: " + str(len(crvgScheduledRules.keys())), "gray")

                actuatedRulesCounter = 0

                #flash("Executing actions for rooms...", "yellow")


                # Executing the rules per each room
                # In the case I have the same action category, I'll take the action with higher priority
                loserRules = {}
                loserRules[self.simulationParameters["time"]] = {}
                loserRules[self.simulationParameters["time"]][self.simulationParameters["stateNumber"]] = {}
                for roomName in roomScheduledRules.keys():
                    #flash("Room [" + building.buildingName + "." + roomName + "]...", "blue")
                    ruleList = roomScheduledRules[roomName]

                    #Let us order by rule priority
                    ruleList = sorted(ruleList, key=lambda rule: rule.getPriority(), reverse=True)

                    alreadyAppliedCategories = []
                    loserRulesList = []

                    for rule in ruleList:

                        if rule.category not in alreadyAppliedCategories:
                            if len(loserRulesList)>0:
                                loserRules[self.simulationParameters["time"]][self.simulationParameters["stateNumber"]][str(winnerRule)] = loserRulesList
                                loserRulesList = []

                            alreadyAppliedCategories.append(rule.category)
                            self.executeRule(rule)
                            actuatedRulesCounter += 1
                            winnerRule = rule.id
                        else:
                            #flash(building.buildingName + " - Room " + roomName + ", ruleId " + str(
                                #rule.id) + " ignored.")
                            loserRuleDict = {}
                            loserRuleDict["ruleId"] = rule.id
                            loserRuleDict["ruleText"] = "if " + rule.antecedent + " then " + rule.consequent
                            loserRulesList.append(loserRuleDict)


                    if len(loserRulesList)>0:
                        loserRules[self.simulationParameters["time"]][self.simulationParameters["stateNumber"]][str(winnerRule)] = loserRulesList

                    if not os.path.exists("tools/simulation/results/losers"):
                        os.makedirs("tools/simulation/results/losers")
                    if os.path.exists("tools/simulation/results/losers/loser_" + roomName + ".json"):
                        in_file = open("tools/simulation/results/losers/loser_" + roomName + ".json","r")
                        tempJson = json.load(in_file)

                        if self.simulationParameters["time"] not in tempJson:
                            tempJson[self.simulationParameters["time"]] = {}

                        if self.simulationParameters["stateNumber"] not in tempJson[self.simulationParameters["time"]]:
                            tempJson[self.simulationParameters["time"]][self.simulationParameters["stateNumber"]] = {}

                        if self.simulationParameters["stateNumber"] in loserRules[self.simulationParameters["time"]]:
                            tempJson[self.simulationParameters["time"]][self.simulationParameters["stateNumber"]] = loserRules[self.simulationParameters["time"]][self.simulationParameters["stateNumber"]]

                        in_file.close()
                    else:
                        tempJson = loserRules


                    out_file = open("tools/simulation/results/losers/loser_" + roomName + ".json","w")
                    out_file.write(json.dumps(tempJson,separators =(',', ':')))
                    out_file.close()

                #flash("Executing actions for CRV Groups...", "yellow")
                for crvgId in crvgScheduledRules.keys():
                    #flash("Group " + building.buildingName + ".g[" + str(crvgId) + "]...", "blue")
                    ruleList = crvgScheduledRules[crvgId]

                    #Let us order by rule priority
                    ruleList = sorted(ruleList, key=lambda rule: rule.getPriority(), reverse=True)

                    alreadyAppliedCategories = []
                    for rule in ruleList:
                        if rule.category not in alreadyAppliedCategories:
                            alreadyAppliedCategories.append(rule.category)
                            self.executeRule(rule)
                            actuatedRulesCounter += 1
                        else:
                            flash(building.buildingName + " - CRVGroup " + str(crvgId) + ", ruleId " + str(
                                rule.id) + " ignored.")
                            self.notifyIgnoredRule(rule)

        #flash("The actuation process is ended.", "yellow")
        endTimeMilliseconds = long((time.time() + 0.5) * 1000)
        opTimeMilliseconds = endTimeMilliseconds - startTimeMilliseconds
        #flash("RunTimeRuleActuation:::RoomFilter=" + str(self.roomFilter) + "::Time=" + str(
            #opTimeMilliseconds) + "::NumberOfRules:" + str(analyzedRoomCounter) + "::TriggeredRules:" + str(
            #len(triggeredRules)) + "::ActuatedRules:" + str(actuatedRulesCounter) + "::IgnoredRules:" + str(
            #len(triggeredRules) - actuatedRulesCounter))

    def __str__(self):
        return "ActionExecutor: "



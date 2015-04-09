__author__ = 'jacopo'

import sys
import copy
import rest
import time
import datetime
import os
import json
from graphviz import Digraph


def fetchDataFromJSON(roomName):
    in_file = open("../../backend/tools/simulation/results/" + roomName + ".json","r")
    in_data = json.load(in_file)
    return in_data

username = "admin"
password = "brulesAdmin2014"
buildingName = "CSE"

# login ##########################################
response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})
sessionKey = response["sessionKey"]
userUuid = response["userUuid"]


response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {
			'username' : username,
			'buildingName' : buildingName,
			'sessionKey' : sessionKey,
			'userUuid' : userUuid
			})

rooms = response["rooms"]

for room in rooms:
    roomData = fetchDataFromJSON(room["roomName"])
    oldActiveRulesText = []
    simulation=["2014-09-15"]

    statesList = []

    count = 0

    for data in simulation:
        for hour in range(0,24,1):
            activeRules = []
            activeRulesText = []

            for category in roomData[data]["simulation"].items() :
                for activation in category[1]:
                    if float(activation["from"].replace(":",".")) <= hour <= float(activation["to"].replace(":",".")) :
                        activeRules.append(activation)
                        activeRulesText.append(activation["ruleText"])

            count += 1

            if set(oldActiveRulesText) != set(activeRulesText) :
                oldActiveRulesText = activeRulesText
                statesList.append((activeRules,count))
                count = 0



    dot = Digraph(comment='Room Graph')

    endingNodeInded = 0
    startingNodeIndex = -1

    archIndex = 0

    duplicatedStatesList = []
    duplicatedStatesIds = {}
    dupBool = False
    for state in statesList:
        nodeLabel = ""
        archLabel = str(archIndex) +"\n"

        antecedentSet = set()
        for rule in state[0]:
            splittedRule = rule["ruleText"].strip().split("then")
            nodeLabel += splittedRule[1] + "\n"
            archLabel += splittedRule[0] + "\n"

        nodeLabel += "time " + str(state[1])

        for duplicatedState in duplicatedStatesList:
            if duplicatedState == nodeLabel:
                dupBool = True
                break

        if dupBool :
            id = duplicatedStatesIds[nodeLabel]
            dot.edge(str(startingNodeIndex),str(id),str(archLabel))
            startingNodeIndex = id
            dupBool = False
        else:
            dot.node(str(endingNodeInded),nodeLabel)
            dot.edge(str(startingNodeIndex),str(endingNodeInded),str(archLabel))
            duplicatedStatesIds[nodeLabel] = endingNodeInded
            duplicatedStatesList.append(nodeLabel)
            startingNodeIndex = endingNodeInded
            endingNodeInded+=1
        archIndex += 1

    dot.render('room-graph'+str(room)+'.gv', view=True)


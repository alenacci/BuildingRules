__author__ = 'jacopo'

import re
import rest
import os
import json
from networkx import nx
from graphviz import Digraph


def fetchDataFromJSON(roomName):
    in_file = open("../../backend/tools/simulation/results/" + roomName + ".json","r")
    in_data = json.load(in_file)
    return in_data

def fetchLosersFromJSON(roomName):
    if os.path.exists("../../backend/tools/simulation/results/losers/loser_" + roomName + ".json"):
        in_file = open("../../backend/tools/simulation/results/losers/loser_" + roomName + ".json","r")
        in_data = json.load(in_file)
    else:
        in_data = {}
    return in_data

def convertIntToHour(hourInt) :
    strHour = str(hourInt)
    if len(strHour) == 1 :
        strHour = "0" + strHour + ":00"
    else:
        strHour = strHour + ":00"
    return strHour

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
    print room
    roomData = fetchDataFromJSON(room["roomName"])
    losersData = fetchLosersFromJSON(room["roomName"])
    oldActiveRulesText = []
    simulation=["2014-09-15"]

    statesList = []
    categoryState = {}
    count = 0

    for data in simulation:
        loserRulesSet = set()
        for hour in range(0,24,1):
            activeRules = []
            activeRulesText = []
            strHour = convertIntToHour(hour)
            for category in roomData[data]["simulation"].items() :
                for activation in category[1]:
                    if float(activation["from"].replace(":",".")) <= hour <= float(activation["to"].replace(":",".")) :
                        activeRules.append(activation)
                        activeRulesText.append(activation["ruleText"])
                        categoryState[category[0]] = activation["status"]

            count += 1
            if strHour in losersData:
                losersDataHour = losersData[strHour]

                for rule in activeRules:
                    if rule["ruleId"] in losersDataHour:
                        loserRulesList = losersDataHour[rule["ruleId"]]
                        for loserRule in loserRulesList:
                            loserRulesSet.add(loserRule)

            if set(oldActiveRulesText) != set(activeRulesText) :
                oldActiveRulesText = activeRulesText
                statesList.append((activeRules,count,loserRulesSet,categoryState.copy()))
                loserRulesSet = set()
                count = 0



    dot = Digraph(comment='Room Graph')
    G = nx.DiGraph()

    dot.body.extend(['rankdir=LR'])

    dot.attr("node",shape="plaintext")#,color="lightgrey",style="filled")

    endingNodeInded = 0
    startingNodeIndex = -1

    archIndex = 0

    duplicatedStatesList = []
    duplicatedStatesIds = {}
    dupBool = False

    for state in statesList:
        nodeLabel = '<<TABLE BORDER="2" CELLBORDER="1" CELLSPACING="10">'
        nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">ACTUATORS STATE</FONT></TD></TR>'
        archLabel = str(archIndex) +"&#92;n"

        nodeLabel += '<TR><TD BGCOLOR="lightblue">'
        for actuators in state[3].items():
            nodeLabel += actuators[0] +": " +actuators[1] + "<BR/>"

        nodeLabel += "</TD></TR>"

        nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">ACTIVE RULES</FONT></TD></TR>'

        nodeLabel += '<TR><TD BGCOLOR="#98FF98">' #green
        antecedentSet = set()
        for rule in state[0]:
            splittedRule = rule["ruleText"].strip().split("then")
            nodeLabel += splittedRule[1] + "<BR/>"
            antecedentSet.add(splittedRule[0])


        nodeLabel += "</TD></TR>"
        nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">LOSER RULES</FONT></TD></TR>'


        nodeLabel += '<TR><TD BGCOLOR="#F75D59">' #red
        for rule in state[2]:
            splittedRule = rule.strip().split("then")
            nodeLabel += splittedRule[1] + "<BR/>"

        lowerTimes = []
        higherTimes = []
        maxLower = 0
        minHigher = 0
        for antecedent in antecedentSet:
            times = re.findall("[0-9]{2}.[0-9]{2}",antecedent)
            if len(times) > 0 :
                lowerTimes.append(float(times[0]))
                higherTimes.append(float(times[1]))
            else :
                archLabel += antecedent + "\n"

        if lowerTimes and higherTimes :
            maxLower = max(lowerTimes)
            minHigher = min(higherTimes)
            archLabel += "If time is between " + str(maxLower) + " and " + str(minHigher) + "\n"

        nodeLabel += "</TD></TR>"
        nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">TIME </FONT></TD></TR><TR><TD>' + str(state[1]) + " hours</TD></TR>"
        nodeLabel += "</TABLE>>"

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
            G.add_node(endingNodeInded,label=nodeLabel)

            dot.edge(str(startingNodeIndex),str(endingNodeInded),str(archLabel))
            G.add_edge(startingNodeIndex,endingNodeInded,label = archLabel)

            duplicatedStatesIds[nodeLabel] = endingNodeInded
            duplicatedStatesList.append(nodeLabel)
            startingNodeIndex = endingNodeInded
            endingNodeInded+=1
        archIndex += 1


    dot.render('room-graph'+str(room)+'.gv', view=True)

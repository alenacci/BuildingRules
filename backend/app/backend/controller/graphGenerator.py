from random import randint
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.roomGraphSimulator import RoomGraphSimulator
from app.backend.controller.roomsManager import RoomsManager

__author__ = 'jacopo'

from graphviz import Digraph
from networkx import nx
import os
import re
import json

class GraphGenerator:
    def __init__(self):
        pass

    def createGraph(self, buildingName=None, roomName=None, username= None, type=None):
        buildingsManager = BuildingsManager()
        buildingsManager.checkUserBinding(buildingName, username)

        if type=="bbg":
            self.editGraph(buildingName,roomName,type)
        elif type=="minbbg":
            self.editGraph(buildingName,roomName,type)

    def editGraph(self,buildingName=None, roomName=None,type=None):
        if type=="bbg":
            if os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName+"_node.pickle"):
                pass
            else:
                self.generateBBG(buildingName,roomName)
        elif type=="minbbg":
            if os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName+"_actuatorsState.pickle"):
                pass
            else:
                self.generateMinBBG(buildingName,roomName)
        #put here other type
        elif type=="blabla":
            pass


    #generate pickle BBG
    def generateBBG(self, buildingName=None, roomName=None):

        #put here the simulation days
        days=["2014-09-15"]
        #days=["2014-09-15", "2014-09-16","2014-09-17","2014-09-18","2014-09-19"]

        roomsManager = RoomsManager()

        rules = roomsManager.getRules(roomName=roomName,buildingName=buildingName)["rules"]
        temperatureSet = set()
        minTemperature = 10000

        for rule in rules:
            if "antecedent" in rule:
                antecedent = rule["antecedent"]
                temperatures = re.findall("room temperature is between ([0-9]{2})F and ([0-9]{2})F",antecedent)
                if len(temperatures) > 0:

                    if int(temperatures[0][0])<minTemperature :
                        minTemperature = int(temperatures[0][0])
                    temperatureSet.add(temperatures[0])

        externalTemperature = minTemperature - 1

        internalTemperatures = set()

        for temperatures in temperatureSet:
            internalTemperatures.add(int(temperatures[0]))
            internalTemperatures.add(int(temperatures[1]))

        if len(internalTemperatures) == 0:
            internalTemperatures.add(minTemperature-1)

        internalTemperatures = sorted(internalTemperatures)


        simulationTemps = set()
        for i in range(0,len(internalTemperatures)-1):
            simulationTemp = randint(internalTemperatures[i],internalTemperatures[i+1])
            simulationTemps.add(simulationTemp)

        simulationTemps.add(externalTemperature)
        simulationTemps = sorted(simulationTemps)


        simulationResult = {}
        statesList = {}

        count = 0
        loserRulesGlobalList = []
        oldActiveRulesText = []
        for day in days:

            roomSimulator = RoomGraphSimulator(buildingName=buildingName, roomName=roomName, occupancies=[True,False],
                roomTemperatures=simulationTemps, externalTemperatures=simulationTemps, weathers=["Sunny","Cloudy","Rainy"],
                currentDate=day)

            simulationResult[day] = roomSimulator.start()

            losersData = self.fetchLosersFromJSON(roomName)

            #print losersData

            for hour in range(0, 23):
                strHour = self.convertIntToHour(hour)
                statesList[hour] = []

                if hour in simulationResult[day]["simulation"]:

                    for state in simulationResult[day]["simulation"][hour].items():
                        categoryState = {}
                        activeRules = []
                        activeRulesText = []
                        for category in state[1].items():
                            for activation in category[1]:
                                activeRules.append(activation)
                                activeRulesText.append(activation["ruleText"])
                                categoryState[category[0]] = activation["status"]


                        count += 1
                        if strHour in losersData:
                            losersDataHour = losersData[strHour]

                            for rule in activeRules:
                                if rule["ruleId"] in losersDataHour[state[0]]:
                                    #if strHour == "12:00":
                                    #    print losersDataHour[state[0]][rule["ruleId"]]
                                    loserRulesList = losersDataHour[state[0]][rule["ruleId"]]
                                    for loserRule in loserRulesList:
                                        if loserRule not in loserRulesGlobalList:
                                            loserRulesGlobalList.append(loserRule)
                        if strHour == "12:00":
                            print loserRulesGlobalList


                        statesList[hour].append((activeRules,count,loserRulesGlobalList,categoryState.copy()))
                        loserRulesGlobalList = []
                        count = 0

        if not os.path.exists("tools/simulation/results/"): os.makedirs("tools/simulation/results/")
        out_file = open("tools/simulation/results/" + roomName + ".json","w")
        out_file.write(json.dumps(simulationResult, separators=(',', ':')))
        out_file.close()


        G = nx.DiGraph()

        endingNodeIndex = 0

        duplicatedStatesList = []
        duplicatedStatesIds = {}
        dupBool = False

        #dictionary to save the index of the starting nodes with respect to the hour
        startingNodeIndexDict = {}
        archList = {}

        #print statesList
        for hour in range(0,23):
            startingNodeIndexDict[hour] = set()
            archList[hour] = {}

            if not statesList[hour]:
                for startingNodeIndex in startingNodeIndexDict[hour-1]:
                    stateUniqueId = []
                    nodeStatDict = {}

                    #nodeStatDict["time"] = "0"

                    nodeStatDict["activeRules"] = []
                    nodeStatDict["loserRules"] = []

                    #prendo i vecchi actuatorsState
                    oldNodeActuatorsState = G.node[startingNodeIndex]["actuatorsState"]
                    nodeStatDict["actuatorsState"] = sorted(oldNodeActuatorsState)
                    for actuators in oldNodeActuatorsState:
                        stateUniqueId.append(str(actuators))

                    archList[hour][str(stateUniqueId)] = []

                    for duplicatedState in duplicatedStatesList:
                        if duplicatedState == str(stateUniqueId):
                            dupBool = True
                            break

                    if dupBool:
                        id = duplicatedStatesIds[str(stateUniqueId)]
                        startingNodeIndexDict[hour].add(id)
                        if startingNodeIndex != id:
                            G.add_edge(startingNodeIndex,id,label=archList[hour][str(stateUniqueId)])
                        dupBool = False
                    else:
                        G.add_node(endingNodeIndex, nodeStatDict)
                        duplicatedStatesList.append(str(stateUniqueId))
                        duplicatedStatesIds[str(stateUniqueId)] = endingNodeIndex
                        startingNodeIndexDict[hour].add(endingNodeIndex)
                        if startingNodeIndex != endingNodeIndex:
                            G.add_edge(startingNodeIndex,endingNodeIndex,label=archList[hour][str(stateUniqueId)])
                        endingNodeIndex += 1

            for state in statesList[hour]:
                if hour != 0:
                    for startingNodeIndex in startingNodeIndexDict[hour-1]:
                        stateUniqueId = []
                        nodeStatDict = {}

                        #nodeStatDict["time"] = str(state[1])

                        antecedentSet = set()
                        nodeStatList = []
                        for rule in state[0]:
                            splittedRule = rule["ruleText"].strip().split("then")
                            stateUniqueId.insert(0,rule["ruleText"])
                            antecedentSet.add(splittedRule[0])
                            nodeStatList.append(rule)
                        nodeStatDict["activeRules"] = sorted(nodeStatList)


                        nodeStatList = []
                        for rule in state[2]:
                            splittedRule = rule["ruleText"].strip().split("then")
                            antecedentSet.add(splittedRule[0])
                            nodeStatList.append(rule)
                            stateUniqueId.insert(1,rule["ruleText"])
                        nodeStatDict["loserRules"] = sorted(nodeStatList)

                        nodeStatList = []
                        actuatorsStatusDict = {}
                        for actuators in state[3].items():
                            nodeStatList.append(actuators[0]+": " + actuators[1])
                            stateUniqueId.append(str(actuators[0]+": " + actuators[1]))
                            actuatorsStatusDict[actuators[0]] = actuators[1]

                        #prendo i vecchi actuatorsState
                        oldNodeActuatorsState = G.node[startingNodeIndex]["actuatorsState"]

                        for oldNodeActuatorState in oldNodeActuatorsState:
                            splittedOldActuatorState = oldNodeActuatorState.strip().split(": ")
                            if splittedOldActuatorState[0] not in actuatorsStatusDict:
                                nodeStatList.append(oldNodeActuatorState)
                                stateUniqueId.append(str(oldNodeActuatorState))


                        nodeStatDict["actuatorsState"] = sorted(nodeStatList)

                        stateUniqueId = sorted(stateUniqueId)

                        archList[hour][str(stateUniqueId)] = []
                        lowerTimes = []
                        higherTimes = []

                        for antecedent in antecedentSet:
                            times = re.findall("[0-9]{2}.[0-9]{2}",antecedent)
                            if len(times) > 0:
                                lowerTimes.append(float(times[0]))
                                higherTimes.append(float(times[1]))
                            else:
                                archList[hour][str(stateUniqueId)].append(antecedent)

                        if lowerTimes and higherTimes :
                            maxLower = max(lowerTimes)
                            minHigher = min(higherTimes)
                            archList[hour][str(stateUniqueId)].append("If time is between " + str(maxLower) + " and " + str(minHigher))

                        for duplicatedState in duplicatedStatesList:
                            if duplicatedState == str(stateUniqueId):
                                dupBool = True
                                break

                        if dupBool:
                            id = duplicatedStatesIds[str(stateUniqueId)]
                            startingNodeIndexDict[hour].add(id)
                            if startingNodeIndex != id:
                                G.add_edge(startingNodeIndex,id,label=archList[hour][str(stateUniqueId)])
                            dupBool = False
                        else:
                            G.add_node(endingNodeIndex, nodeStatDict)
                            duplicatedStatesList.append(str(stateUniqueId))
                            duplicatedStatesIds[str(stateUniqueId)] = endingNodeIndex
                            startingNodeIndexDict[hour].add(endingNodeIndex)
                            if startingNodeIndex != endingNodeIndex:
                                G.add_edge(startingNodeIndex,endingNodeIndex,label=archList[hour][str(stateUniqueId)])
                            endingNodeIndex += 1

                else:
                    stateUniqueId = []
                    nodeStatDict = {}

                    #nodeStatDict["time"] = str(state[1])

                    antecedentSet = set()
                    nodeStatList = []
                    for rule in state[0]:
                        splittedRule = rule["ruleText"].strip().split("then")
                        stateUniqueId.append(rule["ruleText"])
                        antecedentSet.add(splittedRule[0])
                        nodeStatList.append(rule)
                    nodeStatDict["activeRules"] = sorted(nodeStatList)


                    nodeStatList = []
                    for rule in state[2]:
                        splittedRule = rule["ruleText"].strip().split("then")
                        antecedentSet.add(splittedRule[0])
                        nodeStatList.append(rule)
                        stateUniqueId.append(rule["ruleText"])
                    nodeStatDict["loserRules"] = sorted(nodeStatList)

                    nodeStatList = []
                    for actuators in state[3].items():
                        nodeStatList.append(actuators[0]+": " + actuators[1])
                        stateUniqueId.append(str(actuators[0]+": " + actuators[1]))
                    nodeStatDict["actuatorsState"] = sorted(nodeStatList)

                    stateUniqueId = sorted(stateUniqueId)

                    archList[hour][str(stateUniqueId)] = []
                    lowerTimes = []
                    higherTimes = []

                    for antecedent in antecedentSet:
                        times = re.findall("[0-9]{2}.[0-9]{2}",antecedent)
                        if len(times) > 0:
                            lowerTimes.append(float(times[0]))
                            higherTimes.append(float(times[1]))
                        else:
                            archList[hour][str(stateUniqueId)].append(antecedent)

                    if lowerTimes and higherTimes :
                        maxLower = max(lowerTimes)
                        minHigher = min(higherTimes)
                        archList[hour][str(stateUniqueId)].append("If time is between " + str(maxLower) + " and " + str(minHigher))



                    for duplicatedState in duplicatedStatesList:
                        if duplicatedState == str(stateUniqueId):
                            dupBool = True
                            break


                    if dupBool:
                        id = duplicatedStatesIds[str(stateUniqueId)]
                        startingNodeIndexDict[hour].add(id)
                        G.add_edge(-1,id,label=archList[hour][str(stateUniqueId)])
                        dupBool = False
                    else:
                        G.add_node(endingNodeIndex, nodeStatDict)
                        duplicatedStatesList.append(str(stateUniqueId))
                        duplicatedStatesIds[str(stateUniqueId)] = endingNodeIndex
                        startingNodeIndexDict[hour].add(endingNodeIndex)
                        G.add_edge(-1,endingNodeIndex,label=archList[hour][str(stateUniqueId)])
                        endingNodeIndex += 1

        if not os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName): os.makedirs("tools/simulation/graphs/"+buildingName+"/"+roomName)
        nx.write_gpickle(G,"tools/simulation/graphs/"+buildingName+"/" + roomName + "/room-graph_bbg.pickle")

    #generate minBBG pickle from BBG pickle
    def generateMinBBG(self,buildingName,roomName):
        G = nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_bbg.pickle")

        G2 = nx.DiGraph()

        identicalActuatorsStates = {}
        identicalActuatorsStates[-1] = -1
        for n in G.nodes():
            for n2 in G.nodes():
                if G.node[n] and G.node[n2]:
                    actuatorsStateN = G.node[n]["actuatorsState"]
                    actuatorsStateN2 = G.node[n2]["actuatorsState"]
                    if set(actuatorsStateN) == set(actuatorsStateN2):
                        #UNION OF THE ACTIVE RULES IN THE OVERALL STATE
                        for rule in G.node[n2]["activeRules"]:
                            if str(rule["ruleText"]) not in str(G.node[n]["activeRules"]):
                                G.node[n]["activeRules"].append(rule)

                        #UNION OF THE LOSER RULES IN THE OVERALL STATE
                        for rule in G.node[n2]["loserRules"]:
                            if rule not in G.node[n]["loserRules"]:
                                G.node[n]["loserRules"].append(rule)

                        if n2 not in identicalActuatorsStates:
                            identicalActuatorsStates[n2] = n
            if G.node[n]:
                if identicalActuatorsStates[n] == n :
                    G2.add_node(n,actuatorsState = G.node[n]["actuatorsState"],activeRules=G.node[n]["activeRules"],loserRules = G.node[n]["loserRules"])
            else:
                G2.add_node(n)

        for e in G.edges() :
            archList = G.edge[e[0]][e[1]]["label"]
            if identicalActuatorsStates[e[0]] != identicalActuatorsStates[e[1]]:
                G2.add_edge(identicalActuatorsStates[e[0]],identicalActuatorsStates[e[1]],label=archList)

        if not os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName): os.makedirs("tools/simulation/graphs/"+buildingName+"/"+roomName)
        nx.write_gpickle(G2,"tools/simulation/graphs/"+buildingName+"/" + roomName + "/room-graph_minbbg.pickle")



    def fetchDataFromJSON(self,roomName):
        in_file = open("tools/simulation/results/" + roomName + ".json","r")
        in_data = json.load(in_file)
        return in_data

    def fetchLosersFromJSON(self,roomName):
        if os.path.exists("tools/simulation/results/losers/loser_" + roomName + ".json"):
            in_file = open("tools/simulation/results/losers/loser_" + roomName + ".json","r")
            in_data = json.load(in_file)
        else:
            in_data = {}
        return in_data

    def convertIntToHour(self,hourInt) :
        strHour = str(hourInt)
        if len(strHour) == 1 :
            strHour = "0" + strHour + ":00"
        else:
            strHour = strHour + ":00"
        return strHour

    #draw graph from pickle
    def drawGraphForRoom(self,roomName,buildingName,username,type):
        buildingsManager = BuildingsManager()
        buildingsManager.checkUserBinding(buildingName, username)

        G = nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_" + type + ".pickle")
        dot = Digraph(comment='Room Graph',format="png")

        dot.body.extend(['rankdir=LR'])

        dot.attr("node",shape="plaintext")

        for n in G.nodes():
        #prendo info nodo
            if n == -1:
                nodeLabel = '<<TABLE BORDER="2" CELLBORDER="1" CELLSPACING="10"><TR><TD BGCOLOR="white"><FONT COLOR="black" POINT-SIZE="18">START</FONT></TD></TR></TABLE>>'
                dot.node(str(n),nodeLabel)

            if G.node[n]:
                nodeLabel = '<<TABLE BORDER="2" CELLBORDER="1" CELLSPACING="10">'
                nodeLabel += '<TR><TD BGCOLOR="white"><FONT COLOR="black" POINT-SIZE="18">STATE ID: ' + str(n) +'</FONT></TD></TR>'

                if "actuatorsState" in G.node[n]:
                    actuatorsState = G.node[n]["actuatorsState"]

                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">STATE VARIABLES</FONT></TD></TR>'
                    nodeLabel += '<TR><TD BGCOLOR="lightblue">'
                    for actuators in actuatorsState:
                        nodeLabel += actuators + "<BR/>"

                    nodeLabel += "</TD></TR>"

                if "activeRules" in G.node[n]:
                    activeRules = G.node[n]["activeRules"]
                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">ACTIVE RULES</FONT></TD></TR>'
                    nodeLabel += '<TR><TD BGCOLOR="#98FF98">' #green

                    for rule in activeRules:
                        splittedRuleActive = rule["ruleText"].strip().split("then")
                        if splittedRuleActive[1] not in nodeLabel:
                            nodeLabel += "<B>" + rule["ruleId"] + "</B> - " + splittedRuleActive[1] + "<BR/>"
                        else:
                            splittedLabel = nodeLabel.strip().split("- " + splittedRuleActive[1])
                            nodeLabel = splittedLabel[0] + ", " + "<B>" + rule["ruleId"] + "</B> - " + splittedRuleActive[1] + splittedLabel[1]


                    nodeLabel += "</TD></TR>"

                if "loserRules" in G.node[n]:
                    loserRules = G.node[n]["loserRules"]
                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">LOSER RULES</FONT></TD></TR>'
                    nodeLabel += '<TR><TD BGCOLOR="#F75D59">' #red

                    for rule in loserRules:
                        splittedRule = rule["ruleText"].strip().split("then")
                        nodeLabel += "<B>" + str(rule["ruleId"])+ "</B> - " + splittedRule[1] + "<BR/>"

                    nodeLabel += "</TD></TR>"

                if "time" in G.node[n]:
                    time = G.node[n]["time"]
                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">TIME </FONT></TD></TR><TR><TD>' + time + " hours</TD></TR>"

                nodeLabel += "</TABLE>>"

                dot.node(str(n),nodeLabel)

        for edge in G.edges():
            archList = G.edge[edge[0]][edge[1]]["label"]
            archLabel = ""

            for arch in archList:
                archLabel += arch + "\n"
            dot.edge(str(edge[0]),str(edge[1]),archLabel)

        dot.render("tools/simulation/graphs/"+buildingName+"/" + roomName + "/room-graph", view=True)

        response = {}
        import base64
        with open("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph.png", "rb") as image_file:
            response["image"] = base64.b64encode(image_file.read())
        return response


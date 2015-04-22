from app.backend.controller.buildingSimulator import BuildingSimulator
from app.backend.controller.buildingsManager import BuildingsManager

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

        if type=="node":
            self.editGraph(buildingName,roomName,type)
        elif type=="actuatorsState":
            self.editGraph(buildingName,roomName,type)

    def editGraph(self,buildingName=None, roomName=None,type=None):
        if type=="node":
            if os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName+"_node.pickle"):
                pass
            else:
                self.createGraphIdenticalNode(buildingName,roomName)
        elif type=="actuatorsState":
            if os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName+"_actuatorsState.pickle"):
                pass
            else:
                self.fromNodeToActuatorsState(buildingName,roomName)
        elif type=="blabla":
            pass


    def createGraphIdenticalNode(self, buildingName=None, roomName=None):

        buildingSimulator = BuildingSimulator(occupancyTimeRangeFrom="8:00AM", occupancyTimeRangeTo="6:00PM", buildingName=buildingName, startDate="2014-09-15", numberOfDays=1,
                                              roomFilter=roomName)
        buildingSimulator.start()

        roomData = self.fetchDataFromJSON(roomName)
        losersData = self.fetchLosersFromJSON(roomName)
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
                strHour = self.convertIntToHour(hour)
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

        G = nx.DiGraph()

        endingNodeInded = 0
        startingNodeIndex = -1

        archIndex = 0

        duplicatedStatesList = []
        duplicatedStatesIds = {}
        dupBool = False

        for state in statesList:

            nodeStatDict = {}

            nodeStatList = []
            archList = []
            archList.append(str(archIndex))
            for actuators in state[3].items():

                nodeStatList.append(actuators[0]+": " + actuators[1])
            nodeStatDict["actuatorsState"] = nodeStatList

            antecedentSet = set()
            nodeStatList = []
            for rule in state[0]:
                splittedRule = rule["ruleText"].strip().split("then")
                antecedentSet.add(splittedRule[0])
                nodeStatList.append(splittedRule[1])
            nodeStatDict["activeRules"] = nodeStatList

            nodeStatList = []
            for rule in state[2]:
                splittedRule = rule.strip().split("then")
                nodeStatList.append(splittedRule[1])
            nodeStatDict["loserRules"] = nodeStatList

            lowerTimes = []
            higherTimes = []
            maxLower = 0
            minHigher = 0
            for antecedent in antecedentSet:
                times = re.findall("[0-9]{2}.[0-9]{2}",antecedent)
                if len(times) > 0 :
                    lowerTimes.append(float(times[0]))
                    higherTimes.append(float(times[1]))
                else:
                    archList.append(antecedent)

            if lowerTimes and higherTimes :
                maxLower = max(lowerTimes)
                minHigher = min(higherTimes)
                archList.append("If time is between " + str(maxLower) + " and " + str(minHigher))


            nodeStatDict["time"] = str(state[1])

            for duplicatedState in duplicatedStatesList:
                if duplicatedState == str(nodeStatDict):
                    dupBool = True
                    break

            if dupBool :
                id = duplicatedStatesIds[str(nodeStatDict)]
                G.add_edge(startingNodeIndex,id,label = archList)

                startingNodeIndex = id
                dupBool = False
            else:
                G.add_node(endingNodeInded,nodeStatDict)

                G.add_edge(startingNodeIndex,endingNodeInded,label = archList)

                duplicatedStatesIds[str(nodeStatDict)] = endingNodeInded
                duplicatedStatesList.append(str(nodeStatDict))
                startingNodeIndex = endingNodeInded
                endingNodeInded+=1
            archIndex += 1

        if not os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName): os.makedirs("tools/simulation/graphs/"+buildingName+"/"+roomName)
        nx.write_gpickle(G,"tools/simulation/graphs/"+buildingName+"/" + roomName + "/room-graph_node.pickle")

    def fromNodeToActuatorsState(self,buildingName,roomName):
        G = nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_node.pickle")

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
                        G.node[n]["activeRules"] = list(set.union(set(G.node[n]["activeRules"]),set(G.node[n2]["activeRules"])))
                        #INTERSECTION OF THE LOSER RULES IN THE OVERALL STATE
                        G.node[n]["loserRules"] = list(set.intersection(set(G.node[n]["loserRules"]),set(G.node[n2]["loserRules"])))
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

        print identicalActuatorsStates

        if not os.path.exists("tools/simulation/graphs/"+buildingName+"/"+roomName): os.makedirs("tools/simulation/graphs/"+buildingName+"/"+roomName)
        nx.write_gpickle(G2,"tools/simulation/graphs/"+buildingName+"/" + roomName + "/room-graph_actuatorsState.pickle")



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

    def drawGraphForRoom(self,roomName,buildingName,username,type):
        buildingsManager = BuildingsManager()
        buildingsManager.checkUserBinding(buildingName, username)

        G = nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_" + type + ".pickle")
        dot = Digraph(comment='Room Graph',format="png")

        dot.body.extend(['rankdir=LR'])

        dot.attr("node",shape="plaintext")

        for n in G.nodes():
        #prendo info nodo

            if G.node[n]:
                nodeLabel = '<<TABLE BORDER="2" CELLBORDER="1" CELLSPACING="10">'
                nodeLabel += '<TR><TD BGCOLOR="white"><FONT COLOR="black" POINT-SIZE="18">STATE ID: ' + str(n) +'</FONT></TD></TR>'

                if "actuatorsState" in G.node[n]:
                    actuatorsState = G.node[n]["actuatorsState"]

                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">ACTUATORS STATE</FONT></TD></TR>'
                    nodeLabel += '<TR><TD BGCOLOR="lightblue">'
                    for actuators in actuatorsState:
                        nodeLabel += actuators + "<BR/>"

                    nodeLabel += "</TD></TR>"

                if "activeRules" in G.node[n]:
                    activeRules = G.node[n]["activeRules"]
                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">ACTIVE RULES</FONT></TD></TR>'
                    nodeLabel += '<TR><TD BGCOLOR="#98FF98">' #green

                    for rule in activeRules:
                        nodeLabel += rule + "<BR/>"

                    nodeLabel += "</TD></TR>"

                if "loserRules" in G.node[n]:
                    loserRules = G.node[n]["loserRules"]
                    nodeLabel += '<TR><TD BGCOLOR="black"><FONT COLOR="white" POINT-SIZE="18">LOSER RULES</FONT></TD></TR>'
                    nodeLabel += '<TR><TD BGCOLOR="#F75D59">' #red

                    for rule in loserRules:
                        nodeLabel += rule + "<BR/>"

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


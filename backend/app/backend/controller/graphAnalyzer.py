from networkx import nx
from app.backend.controller.roomsManager import RoomsManager

class GraphAnalyzer:

    def __init__(self):
        pass

    def analyzeAll(self,buildingName, roomName):
        returnInfo = {}
        returnInfo["uselessRules"] = self.analyzeLoserRules(buildingName,roomName)
        returnInfo["uncontrolledStates"] = self.analyseUncontrolledStates(buildingName,roomName)
        returnInfo["uncontrolledActuators"] = self.analyzeUncontrolledActuators(buildingName,roomName)
        returnInfo["cycleExistence"] = self.analyzeCycleExistence(buildingName,roomName)
        return returnInfo

    def analyseUncontrolledStates(self,buildingName,roomName):
        G = self.readFromBbg(buildingName,roomName)

        uncontrolledStates = set()
        for n in G.nodes():
            if "activeRules" not in G.node[n]:
                if n != -1:
                    uncontrolledStates.add(n)
            else:
                if not G.node[n]["activeRules"]:
                    uncontrolledStates.add(n)
        return list(uncontrolledStates)

    def analyzeLoserRules(self, buildingName, roomName):
        G = self.readFromMinBbg(buildingName,roomName)
        loserRules = set()
        for n in G.nodes():
            if "loserRules" in G.node[n]:
                for loserRule in G.node[n]["loserRules"]:
                    loserRules.add(str(loserRule["ruleId"]))
        for n in G.nodes():
            if "activeRules" in G.node[n]:
                for activeRule in G.node[n]["activeRules"]:
                    if str(activeRule["ruleId"]) in loserRules:
                        loserRules.remove(activeRule["ruleId"])
        return list(loserRules)

    def analyzeUncontrolledActuators(self, buildingName, roomName):
        G = self.readFromMinBbg(buildingName,roomName)
        roomsManager = RoomsManager()
        actionList = roomsManager.getActions(roomName,buildingName)["actions"]
        actionListCopy = list(actionList)
        actionExcluded = ["SEND_COMPLAIN", "DANGER"]
        for action in actionList:
            for n in G.nodes():
                if "actuatorsState" in G.node[n]:
                    actionCategory = str(action["category"])
                    if action["category"] == "APP_PROJECTOR":
                        actionCategory = "PROJECTOR"
                    if action["category"] == "APP_COMPUTER":
                        actionCategory = "COMPUTER"
                    if action["category"] == "APP_DESKLIGHT":
                        actionCategory = "DESKLIGHT"
                    if action["category"] == "APP_PRINTER":
                        actionCategory = "PRINTER"
                    if action["category"] == "APP_DISPLAYMONITOR":
                        actionCategory = "DISPLAYMONITOR"
                    if action["category"] == "APP_AUDIO":
                        actionCategory = "AUDIO"
                    if action["category"] == "HVAC_TEMP":
                        actionCategory = "TEMPERATURE"
                    if action["category"] == "HVAC_HUM":
                        actionCategory = "HUMIDITY"
                    if action["category"] == "APP_COFFEE":
                        actionCategory = "COFFEE"

                    if actionCategory in actionExcluded:
                        if action in actionListCopy:
                            actionListCopy.remove(action)
                    elif actionCategory in str(G.node[n]["actuatorsState"]):
                        if action in actionListCopy:
                            actionListCopy.remove(action)

        actionUncontrolled = set()
        for action in actionListCopy:
            actionUncontrolled.add(action["category"])
        return list(actionUncontrolled)

    def analyzeCycleExistence(self, buildingName, roomName):
        G = self.readFromMinBbg(buildingName,roomName)
        if not list(nx.simple_cycles(G)):
            return "No Cycle Found - Your room may be unstable"
        return "Cycle Found - Your room seems to be stable"



    def readFromBbg(self, buildingName, roomName):
        return nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_bbg.pickle")

    def readFromMinBbg(self, buildingName, roomName):
        return nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_minbbg.pickle")
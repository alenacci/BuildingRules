from networkx import nx

class GraphAnalyzer:

    def __init__(self):
        pass

    def analyzeAll(self,buildingName, roomName):
        returnInfo = {}
        returnInfo["uselessRules"] = self.analyzeLoserRules(buildingName,roomName)
        return returnInfo

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

    def readFromBbg(self, buildingName, roomName):
        return nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_node.pickle")

    def readFromMinBbg(self, buildingName, roomName):
        return nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_actuatorsState.pickle")
from networkx import nx

class GraphAnalyzer:

    def __init__(self):
        pass

    def analyzeAll(self,buildingName, roomName):
        self.analyzeLoserRules(buildingName,roomName)

    def analyzeLoserRules(self, buildingName, roomName):
        G = self.readFromMinBbg(buildingName,roomName)
        loserRules = []
        for n in G.nodes():
            print G.node[n]["loserRules"]
        return

    def readFromBbg(self, buildingName, roomName):
        return nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_node.pickle")

    def readFromMinBbg(self, buildingName, roomName):
        return nx.read_gpickle("tools/simulation/graphs/" +buildingName+"/"+ roomName + "/room-graph_actuatorsState.pickle")
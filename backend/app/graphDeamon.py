__author__ = 'jacopo'

from app.backend.commons.console import flash

from app.backend.controller.graphGenerator import *
from app.backend.controller.graphAnalyzer import *

def start():
    flash("BuildingRules GraphDeamon is active...")

    __ANALISYS_PATH = "../apps/frontend/tmp/analysis/"

    buildingsManager = BuildingsManager()
    graphGenerator = GraphGenerator()

    graphAnalyzer = GraphAnalyzer()

    rooms = buildingsManager.getRooms(buildingName="JOL")["rooms"]

    while (1):
        try:
            for room in rooms:
                graphGenerator.generateBBG(buildingName="JOL", roomName=room["roomName"])
                graphGenerator.generateMinBBG(buildingName="JOL", roomName=room["roomName"])

                #graphGenerator.drawGraphForRoom(buildingName="JOL", roomName=room["roomName"],username="admin",type="bbg")

                analisysDict = graphAnalyzer.analyzeAll(buildingName="JOL", roomName=room["roomName"])

                if not os.path.exists(__ANALISYS_PATH):
                    os.makedirs(__ANALISYS_PATH)

                with open(__ANALISYS_PATH + room["roomName"] + ".json","wb") as fp:
                    json.dump(analisysDict,fp=fp)

        except Exception as e:
            import logging

            logging.basicConfig(filename='logs/deamon.log')
            logging.getLogger().addHandler(logging.StreamHandler())
            logging.exception("")
            flash(e.message)

        time.sleep(600)

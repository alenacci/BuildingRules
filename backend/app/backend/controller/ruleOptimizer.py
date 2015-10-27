__author__ = 'andreuke'

from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.model.truthTable.truthTable import TruthTable
from app.backend.model.room import Room

class RuleOptimizer:
    def __init__(self, building):
        self.building = building
        self.truthTables = {}
        pass

    def run(self):
        buildingsManager = BuildingsManager()
        rooms = buildingsManager.getRooms(buildingName=self.building)["rooms"]

        for room in rooms:
            roomName = room["roomName"]
            # TODO: remove if and reindent !!!TEMPORARY!!!
            if  roomName == '2111':
                room = Room(roomName, _building_)
                truthTable = TruthTable(room)
                self.truthTables[roomName] = truthTable
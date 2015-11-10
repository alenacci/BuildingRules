__author__ = 'andreuke'

from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.model.truthTable.truthTable import TruthTable
from app.backend.model.room import Room


class RuleOptimizer:
    def __init__(self, building, room):
        self.building = building
        self.room = room
        self.truthTables = {}
        pass

    def run(self):
        # buildingsManager = BuildingsManager()
        # rooms = buildingsManager.getRooms(buildingName=self.building)["rooms"]

        # for r in rooms:
            # roomName = r['roomName']
            # # TODO: remove if and reindent !!!TEMPORARY!!!
            # if  roomName == self.room:
        roomName = self.room
        room = Room(roomName, self.building)
        truthTable = TruthTable(room)
        # self.truthTables[roomName] = truthTable
        return truthTable

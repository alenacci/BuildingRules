# ###########################################################
#
# BuildingRules Project
# Politecnico di Milano
# Author: Alessandro A. Nacci
#
# This code is confidential
# Milan, March 2014
#
############################################################
from operator import itemgetter

import time
import os
import string
import random

from app.backend.commons.inputDataChecker import checkData
from app.backend.controller.actionExecutor import ActionExecutor


class RoomGraphSimulator:
    def __init__(self, buildingName=None, roomName=None, occupancies=None,
                 roomTemperatures=None, externalTemperatures=None, weathers=None, time=None, currentDate=None):

        checkData(locals())

        self.buildingName = buildingName
        self.roomName = roomName
        self.occupancies = occupancies
        self.roomTemperatures = roomTemperatures
        self.externalTemperatures = externalTemperatures
        self.weathers = weathers
        self.time = time
        self.currentDate = currentDate

    def start(self):

        simulationBufferFolder = "tools/simulation/tmp/"
        if not os.path.exists(simulationBufferFolder): os.makedirs(simulationBufferFolder)
        simulationBufferFileName = self.__addPrefixToFileName(self.buildingName + "_" + self.roomName + ".sim")
        simulationBufferFilePath = (simulationBufferFolder + "/" + simulationBufferFileName).replace("//", "/")
        os.remove(simulationBufferFilePath) if os.path.exists(simulationBufferFilePath) else None

        if os.path.exists("tools/simulation/results/losers/loser_"+self.roomName+".json"):
            os.remove("tools/simulation/results/losers/loser_"+self.roomName+".json")

        count = 0
        gantt = {}

        for hour in range(0, 23):
            for minute in range(0, 60, 60):
                h = str(hour) if len(str(hour)) == 2 else "0" + str(hour)
                m = str(minute) if len(str(minute)) == 2 else "0" + str(minute)
                currentTime = h + ":" + m

                for roomTemperature in self.roomTemperatures:
                    for externalTemperature in self.externalTemperatures:
                        for occupancy in self.occupancies:
                            for weather in self.weathers:

                                simulationParameters = {}
                                simulationParameters['roomTemperature'] = roomTemperature
                                simulationParameters['occupancy'] = occupancy
                                simulationParameters['day'] = self._getCurrentDay()
                                simulationParameters['date'] = self._getCurrentDate()
                                simulationParameters['weather'] = weather
                                simulationParameters['externalTemperature'] = externalTemperature
                                simulationParameters['time'] = currentTime
                                simulationParameters['resultsBufferFile'] = simulationBufferFilePath
                                simulationParameters['stateNumber'] = count

                                roomFilter = [{'buildingName': self.buildingName, 'roomName': self.roomName}]

                                actionExecutor = ActionExecutor(simulationParameters=simulationParameters, roomFilter=roomFilter)
                                actionExecutor.start()
                                count += 1


                if os.path.exists(simulationBufferFilePath):
                    f = open(simulationBufferFilePath)
                    lines = f.readlines()
                    f.close()

                    os.remove(simulationBufferFilePath) if os.path.exists(simulationBufferFilePath) else None

                    actionTargets = set()
                    actionTargetsRecordsNumber = {}
                    timeRecords = []

                    for line in lines:

                        record = line.replace("\n", "").split(";")
                        timeRecords.append(record)
                        actionTargets.add(record[2])
                        if record[2] not in actionTargetsRecordsNumber.keys(): actionTargetsRecordsNumber[record[2]] = 0
                        actionTargetsRecordsNumber[record[2]] += 1

                    I_TARGET = 2
                    I_STATUS = 3
                    I_RULE_ID = 4
                    I_RULE_TEXT = 5
                    I_RULE_STATE_NUMBER = 6

                    gantt[hour] = {}
                    sorted(timeRecords,key=itemgetter(I_RULE_STATE_NUMBER))

                    interval = {}

                    for record in timeRecords:
                        interval["status"] = record[I_STATUS]
                        interval["ruleId"] = record[I_RULE_ID]
                        interval["ruleText"] = record[I_RULE_TEXT]
                        stateNumber = record[I_RULE_STATE_NUMBER]

                        if stateNumber not in gantt[hour]:
                            gantt[hour][stateNumber] = {}

                        if record[I_TARGET] not in gantt[hour][stateNumber]:
                            gantt[hour][stateNumber][record[I_TARGET]] = []

                        gantt[hour][stateNumber][record[I_TARGET]].append(
                            {"status": interval["status"],
                             "ruleId": interval["ruleId"], "ruleText": interval["ruleText"]})




        return {"simulation": gantt}

    def _getCurrentDate(self):
        if not self.currentDate:
            return str(time.strftime("%d/%m"))

        from datetime import datetime

        return datetime.strptime(self.currentDate, '%Y-%m-%d').strftime("%d/%m")

    def _getCurrentDay(self):

        from datetime import datetime

        if self.currentDate:

            currentDayInt = datetime.strptime(self.currentDate, '%Y-%m-%d').weekday()
        else:
            currentDayInt = datetime.today().weekday()

        if currentDayInt == 0: return "Monday"
        if currentDayInt == 1: return "Tuesday"
        if currentDayInt == 2: return "Wednesday"
        if currentDayInt == 3: return "Thursday"
        if currentDayInt == 4: return "Friday"
        if currentDayInt == 5: return "Saturday"
        if currentDayInt == 6: return "Sunday"


    def _getTimeInMinutes(self, timeString):

        plainTime = timeString.replace("AM", "").replace("PM", "").replace("am", "").replace("pm", "").strip().replace(
            ":", ".")

        hour = int(plainTime[:plainTime.find(".")])
        minute = int(plainTime[plainTime.find(".") + 1:])

        if "PM" in timeString or "pm" in timeString:
            hour += 12

        return hour * 60 + minute


    def __id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def __addPrefixToFileName(self, filename):

        from hashlib import md5
        from time import localtime

        return "%s_%s_%s" % (self.__id_generator(), md5(str(localtime())).hexdigest(), filename)

    def __str__(self):
        return "RoomSimulator: "





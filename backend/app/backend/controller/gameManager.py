############################################################
#
# BuildingRules Project 
# Politecnico di Milano
# Author: Jacopo Fiorenza, Andrea Mariani
#
# This code is confidential
# Milan, March 2014
#
############################################################
import re
import datetime
import sched
import time
import thread
import operator
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.roomSimulator import RoomSimulator
from app.backend.controller.roomsManager import RoomsManager
from app.backend.controller.notificationsManager import NotificationsManager
from app.backend.controller.usersManager import UsersManager


class GameManager:
    statusDict = {}
    statusDictControl = {}
    statusAction = {}
    dataTarget = {}
    targetTemp = {}
    targetHum = {}
    roomList = []
    scores = {}
    roomHappiness = {}
    buildingUsers = []

    def __init__(self):
        pass


    def saveSim(self, resultSim, occupancyTimeRangeFrom, roomName):

        if "PM" in occupancyTimeRangeFrom:
            otrf = occupancyTimeRangeFrom.replace(" PM","")
            otrf = float(otrf.replace(":","."))
            otrf += 12.0
        else :
            otrf = occupancyTimeRangeFrom.replace(" AM","")
            otrf = float(otrf.replace(":","."))

        print resultSim
        data = []
        self.statusAction[roomName] = {}
        for target in resultSim["simulation"].keys():
            self.statusAction[roomName][target] = ""
            data.append(target)
            for bar in resultSim["simulation"][target]:
                timeFrom = float(bar["from"].replace(":","."))
                timeTo = float(bar["to"].replace(":","."))
                print str(timeFrom) + str(otrf) + str(timeTo)
                if timeFrom <= otrf < timeTo:
                    self.statusAction[roomName][target] = bar["status"]
        self.dataTarget[roomName] = data
        print self.statusAction[roomName]

    def initValues(self, buildingName, username):
        buildingsManager = BuildingsManager()
        buildingsManager.checkUserBinding(buildingName, username)
        response = buildingsManager.getRooms(buildingName=buildingName, username=username)

        rooms = response["rooms"]
        print rooms
        for room in rooms:
            valuesDict = {"ExtTemp" : "70F", "RoomTemp" : "66F", "Hum" : "20%" ,"Weather" : "sunny", "Power" : 0}
            valuesDictControl = {"ExtTemp" : 70, "RoomTemp" : 66, "Hum" : 20,"Weather" : "sunny", "Power" : 0}
            self.statusDict[room["roomName"]] = valuesDict
            self.statusDictControl[room["roomName"]] = valuesDictControl
            self.statusAction[room["roomName"]] = {}
            self.dataTarget[room["roomName"]] = []
            self.roomList.append(room["roomName"])
            self.roomHappiness[room["roomName"]] = {"you":True,"manager":True}
        thread.start_new_thread(self.threadExec,(buildingName, ))
        #thread.start_new_thread(self.mailServiceExec,())


    def upgradeValues(self, roomName, buildingName, username):
        if len(self.statusDict)==0 :
            self.initValues(buildingName,username)

        buildingsManager = BuildingsManager()
        roomsManager = RoomsManager()
        rooms = buildingsManager.getRooms(buildingName)
        self.buildingUsers = []
        for room in rooms["rooms"]:
            users = roomsManager.getUsers(room["roomName"],buildingName)
            for user in users["users"]:
                if user["username"] not in self.buildingUsers:
                    self.buildingUsers.append(user["username"])

        if username not in self.scores:
            self.scores[username] = 0

        returnInfo= {}
        returnInfo["statusDict"] =self.statusDict[roomName]
        returnInfo["statusAction"] = self.statusAction[roomName]
        returnInfo["target"] = self.dataTarget[roomName]
        returnInfo["score"] = self.scores[username]
        returnInfo["ranking"] = self.scores
        returnInfo["happiness"] = self.roomHappiness[roomName]
        returnInfo["usernames"] = self.buildingUsers
        now = datetime.datetime.now()
        returnInfo["time"]= str(now.hour)+":"+str(now.minute)
        return returnInfo

    def powerSimulator(self, roomName):

        power = 0
        hvacPower = 1500
        flagHvac = 0
        lightPower = 5
        coffeePower = 800
        printerPower = 100
        computerPower = 150
        audioPower = 80
        displayMonitorPower = 70
        projectorPower = 200

        if roomName in self.statusAction:

            if "RoomTemp" in self.statusDictControl[roomName] and roomName in self.targetTemp:

                if str(self.targetTemp[roomName]) != str(self.statusDictControl[roomName]["RoomTemp"]):
                    flagHvac = 1

            if "Hum" in self.statusDictControl[roomName] and roomName in self.targetHum:

                if str(self.targetHum[roomName]) != str(self.statusDictControl[roomName]["Hum"]):
                    flagHvac = 1

            power += (hvacPower*flagHvac)
            #print self.statusAction
            if "LIGHT" in self.statusAction[roomName] :
                if self.statusAction[roomName]["LIGHT"] == "ON" :
                    power += lightPower

            if "DESKLIGHT" in self.statusAction[roomName] :
                if self.statusAction[roomName]["DESKLIGHT"] == "ON" :
                    power += lightPower

            if "COFFEE" in self.statusAction[roomName] :
                if self.statusAction[roomName]["COFFEE"] == "ON" :
                    power += coffeePower

            if "PRINTER" in self.statusAction[roomName] :
                if self.statusAction[roomName]["PRINTER"] == "ON" :
                    power += printerPower

            if "COMPUTER" in self.statusAction[roomName] :
                if self.statusAction[roomName]["COMPUTER"] == "ON" :
                    power += computerPower

            if "AUDIO" in self.statusAction[roomName] :
                if self.statusAction[roomName]["AUDIO"] == "ON" :
                    power += audioPower

            if "PROJECTOR" in self.statusAction[roomName] :
                if self.statusAction[roomName]["PROJECTOR"] == "ON" :
                    power += projectorPower

            if "DISPLAYMONITOR" in self.statusAction[roomName] :
                if self.statusAction[roomName]["DISPLAYMONITOR"] == "ON" :
                    power += displayMonitorPower


            self.statusDict[roomName]["Power"] = power
            self.statusDictControl[roomName]["Power"] = power



    def tempSimulator(self, roomName):

        deltaTemp = 0
        hvacTemp = 1
        windowTemp = 1

        if roomName in self.statusAction:
            if "WINDOWS" in self.statusAction[roomName] :
                if self.statusAction[roomName]["WINDOWS"] == "OPEN":
                    if self.statusDictControl[roomName]["RoomTemp"]> self.statusDictControl[roomName]["ExtTemp"]:
                        deltaTemp-=windowTemp
                    elif self.statusDictControl[roomName]["RoomTemp"]< self.statusDictControl[roomName]["ExtTemp"]:
                        deltaTemp+=windowTemp

            #HVAC temperature change
            if "TEMPERATURE" in self.statusAction[roomName] :
                #check temp (es 64F-70F) -> if is out of range..flagHvac=1 TODO
                temps = re.findall("[0-9]{2}F-[0-9]{2}F",self.statusAction[roomName]["TEMPERATURE"])

                temperatures = temps[0].strip().split("-")

                newTemps = []
                newTemps.append(temperatures[0].replace("F",""))
                newTemps.append(temperatures[1].replace("F",""))

                if self.statusDictControl[roomName]["RoomTemp"]<newTemps[0]:
                    self.targetTemp[roomName] = newTemps[0]
                if newTemps[1] < self.statusDictControl[roomName]["RoomTemp"]:
                    self.targetTemp[roomName] = newTemps[1]

            if "RoomTemp" in self.statusDictControl[roomName] and roomName in self.targetTemp:
                if str(self.targetTemp[roomName]) != str(self.statusDictControl[roomName]["RoomTemp"]):
                    if self.statusDictControl[roomName]["RoomTemp"] < self.targetTemp[roomName]:
                        deltaTemp += hvacTemp
                    elif self.statusDictControl[roomName]["RoomTemp"] > self.targetTemp[roomName]:
                        deltaTemp -= hvacTemp


            if deltaTemp >0:
                self.statusDictControl[roomName]["RoomTemp"]+=deltaTemp

                self.statusDict[roomName]["RoomTemp"] = str(self.statusDictControl[roomName]["RoomTemp"]) + "F"



    def humSimulator(self,roomName):

        deltaHum = 0
        hvacHum = 1

        if roomName in self.statusAction:
            #HVAC humidity change
            if "HUMIDITY" in self.statusAction[roomName] :
                hums = re.findall("[0-9]{2}%-[0-9]{2}%",self.statusAction[roomName]["HUMIDITY"])
                humidities = hums[0].strip().split("-")

                newHums = []
                newHums.append(humidities[0].replace("%",""))
                newHums.append(humidities[1].replace("%",""))
                print newHums

                if self.statusDictControl[roomName]["Hum"]<newHums[0]:
                    self.targetHum[roomName] = newHums[0]
                if newHums[1] < self.statusDictControl[roomName]["Hum"]:
                    self.targetHum[roomName] = newHums[1]

            if "Hum" in self.statusDictControl[roomName] and roomName in self.targetHum:
                if str(self.targetHum[roomName]) != str(self.statusDictControl[roomName]["Hum"]):
                    if self.statusDictControl[roomName]["Hum"] < self.targetHum[roomName]:
                        deltaHum += hvacHum
                    elif self.statusDictControl[roomName]["Hum"] > self.targetHum[roomName]:
                        deltaHum -= hvacHum

            if deltaHum >0:
                self.statusDictControl[roomName]["Hum"]+=deltaHum
                self.statusDict[roomName]["Hum"] = str(self.statusDictControl[roomName]["Hum"]) + "%"


    def simulate(self,buildingName):
        for room in self.roomList:
            now = datetime.datetime.now()
            h = now.hour
            hTo = 0
            if(h > 12):
                hTo = str(h-11)+":00 PM"
                h = str(h-12)+":00 PM"
            else:
                hTo = str(h+1)+":00 AM"
                h = str(h)+":00 AM"
            roomSimulator = RoomSimulator(buildingName=buildingName, roomName=room,
                                              occupancyTimeRangeFrom=h,
                                              occupancyTimeRangeTo=hTo, roomTemperature=self.statusDict[room]["RoomTemp"],
                                              externalTemperature=self.statusDict[room]["ExtTemp"], weather=self.statusDict[room]["Weather"])
            self.saveSim(roomSimulator.start(),h,room)
            self.tempSimulator(room)
            self.humSimulator(room)
            self.powerSimulator(room)
            self.showRanking()

            roomsManager = RoomsManager()
            users = roomsManager.getUsers(room,buildingName)
            for user in users["users"]:
                self.getScores(user["username"],room)

    def getScores(self,username,roomName):
        if username not in self.scores:
            self.scores[username] = 0
        youHappy = True
        managerHappy = True

        if "TEMPERATURE" in self.statusAction[roomName] and "WINDOWS" in self.statusAction[roomName]:
            if self.statusAction[roomName]["WINDOWS"] == "OPEN":
                managerHappy = False

        if  self.statusDictControl[roomName]["RoomTemp"] < 64 and self.statusDictControl[roomName]["RoomTemp"]> 72 :
            youHappy = False
            self.scores[username] -= 1
        else:
            self.scores[username] += 1

        if self.statusDictControl[roomName]["Power"] > 3000 :
            managerHappy = False
            self.scores[username] -= 1
        else:
            self.scores[username] += 1
        print self.scores[username]

        self.roomHappiness[roomName]["you"] = youHappy
        self.roomHappiness[roomName]["manager"] = managerHappy

    def sendSummaryByEmail(self):
        print "sendSummaryByEmail"
        notificationManager = NotificationsManager()

        if len(self.buildingUsers) != 0:
            from app.backend.model.user import User
            if len(self.buildingUsers) !=0 :
                for notifUser in self.buildingUsers:
                    print "NOTIFUSER = " + notifUser
                    user = User(username=notifUser)
                    user.retrieve()
                    userUuid = user.uuid
                    message = ""
                    rooms = user.getRoomsDict()
                    if len(rooms)!= 0:
                        for room in rooms:
                            if room["buildingName"] == "HG":
                                roomName = room["roomName"]
                                message += "ROOM " + str(roomName) + " STATUS\n"
                                message += "External Temperature: " + str(self.statusDict[roomName]["ExtTemp"]) + "\n"
                                message += "Room Temperature: " + str(self.statusDict[roomName]["RoomTemp"]) + "\n"
                                message += "Humidity: " + str(self.statusDict[roomName]["Hum"]) + "\n"
                                message += "Weather: " + str(self.statusDict[roomName]["Weather"]) + "\n"
                                message += "Power: " + str(self.statusDict[roomName]["Power"]) + "\n"
                                message += "FEELINGS\n"
                                message += "Your Feeling: "
                                if self.roomHappiness[roomName]["you"]: message += "Happy\n"
                                else: message += "Sad\n"
                                message += "BuildingManager Feeling: "
                                if self.roomHappiness[roomName]["manager"]: message += "Happy\n\n"
                                else: message += "Sad\n\n"
                    message += "RANKING\n"
                    ranking = self.showRanking().items()
                    for item in ranking:
                        message += str(item[0]) + " " + str(item[1]) + "\n"
                    notificationManager.sendNotificationByEmail(userUuid,"Building Summary",message)

    def mailServiceExec(self,scheduler = None):
        if scheduler is None:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(90, 1, self.mailServiceExec, ([scheduler]))
            scheduler.run()
        if scheduler is not None:
            scheduler.enter(90, 1, self.mailServiceExec, ([scheduler]))

        self.sendSummaryByEmail()

    def threadExec(self,buildingName,scheduler = None):

        if scheduler is None:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(60, 1, self.threadExec, ([buildingName, scheduler]))
            scheduler.run()
        if scheduler is not None:
            scheduler.enter(60, 1, self.threadExec, ([buildingName, scheduler]))

        self.simulate(buildingName)

    def showRanking(self):
        sortedScores = sorted(self.scores.items(), key=operator.itemgetter(1))
        print sortedScores
        for (i,j) in sortedScores:
            self.scores[i] = j
        return self.scores


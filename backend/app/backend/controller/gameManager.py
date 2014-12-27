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
import json
import os
import random
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


class GameManager:
    statusDict = {}
    statusDictControl = {}
    statusAction = {}
    dataTarget = {}
    targetTemp = {}
    targetHum = {}
    roomList = []
    scores = {}
    sortedScores = []
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
        response = buildingsManager.getRooms(buildingName=buildingName)

        rooms = response["rooms"]
        for room in rooms:
            self.roomList.append(room["roomName"])

        successData = self.dataRestore()
        self.scoresRestore()
        print self.statusDictControl
        print self.statusDict
        if not successData:
            weather = random.randrange(1,3,1)
            if weather == 1:
                w = "sunny"
            if weather == 2:
                w="cloudy"
            if weather == 3:
                w = "rainy"
            extTemp = random.randrange(55,68,1)
        for room in rooms:
            if not successData:
                temp = random.randrange(55,80,1)
                hum = random.randrange(20,45,1)
                valuesDict = {"ExtTemp" : str(extTemp)+"F", "RoomTemp" : str(temp)+"F", "Hum" : str(hum)+"%" ,"Weather" : w, "Power" : 0}
                valuesDictControl = {"ExtTemp" : extTemp, "RoomTemp" : temp, "Hum" : hum,"Weather" : w, "Power" : 0}
                self.statusDict[room["roomName"]] = valuesDict
                self.statusDictControl[room["roomName"]] = valuesDictControl

            self.statusAction[room["roomName"]] = {}
            self.dataTarget[room["roomName"]] = []

            self.roomHappiness[room["roomName"]] = {"you":True,"whyYou":"","manager":True,"whyManager":""}
        thread.start_new_thread(self.threadExec,(buildingName, ))
        thread.start_new_thread(self.mailServiceExec,())


    def upgradeValues(self, roomName, buildingName, username):

        self.scoresRestore()
        self.dataRestore()

        if len(self.statusDict)==0 or len(self.statusDictControl)==0 :
            self.initValues(buildingName,username)

        buildingsManager = BuildingsManager()
        roomsManager = RoomsManager()
        rooms = buildingsManager.getRooms(buildingName)

        for room in rooms["rooms"]:
            users = roomsManager.getUsers(room["roomName"],buildingName)
            for user in users["users"]:
                if user["username"] not in self.buildingUsers and '--' not in user["email"]:
                    self.buildingUsers.append(user["username"])

        if username not in self.scores:
            self.scores[username] = 0
            self.scoresDump()

        sortedScores = sorted(self.scores.items(), key=operator.itemgetter(1),reverse=True)
        scores = ""
        for item in sortedScores:
            scores += str(item[0])+" - "+str(item[1])+" <br/> <br/>"
        returnInfo= {}
        returnInfo["statusDict"] =self.statusDict[roomName]
        returnInfo["statusAction"] = self.statusAction[roomName]
        returnInfo["target"] = self.dataTarget[roomName]
        returnInfo["score"] = self.scores[username]
        returnInfo["ranking"] = scores
        returnInfo["happiness"] = self.roomHappiness[roomName]
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

            if len(self.statusDictControl)!= 0 :
                self.dataDump()
            else :
                self.dataRestore()



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
                    self.tempDump()
                if newTemps[1] < self.statusDictControl[roomName]["RoomTemp"]:
                    self.targetTemp[roomName] = newTemps[1]
                    self.tempDump()

            self.tempRestore()
            if "RoomTemp" in self.statusDictControl[roomName] and roomName in self.targetTemp:
                if str(self.targetTemp[roomName]) != str(self.statusDictControl[roomName]["RoomTemp"]):
                    if self.statusDictControl[roomName]["RoomTemp"] < int(self.targetTemp[roomName]):
                        deltaTemp += hvacTemp
                    elif self.statusDictControl[roomName]["RoomTemp"] > int(self.targetTemp[roomName]):
                        deltaTemp -= hvacTemp


            if deltaTemp !=0:
                self.statusDictControl[roomName]["RoomTemp"]+=deltaTemp
                self.statusDict[roomName]["RoomTemp"] = str(self.statusDictControl[roomName]["RoomTemp"]) + "F"

            if len(self.statusDictControl)!= 0 :
                self.dataDump()
            else :
                self.dataRestore()



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
                    self.humidityDump()
                if newHums[1] < self.statusDictControl[roomName]["Hum"]:
                    self.targetHum[roomName] = newHums[1]
                    self.humidityDump()

            self.humidityRestore()
            if "Hum" in self.statusDictControl[roomName] and roomName in self.targetHum:
                if str(self.targetHum[roomName]) != str(self.statusDictControl[roomName]["Hum"]):
                    if self.statusDictControl[roomName]["Hum"] < int(self.targetHum[roomName]):
                        deltaHum += hvacHum
                        print "alzo"
                    elif self.statusDictControl[roomName]["Hum"] > int(self.targetHum[roomName]):
                        deltaHum -= hvacHum
                        print "abbasso"
                print str(self.targetHum[roomName])+str(self.statusDictControl[roomName]["Hum"])+str(deltaHum)+"PROVAAA"
            if deltaHum !=0:
                self.statusDictControl[roomName]["Hum"]+=deltaHum
                self.statusDict[roomName]["Hum"] = str(self.statusDictControl[roomName]["Hum"]) + "%"

            if len(self.statusDictControl)!= 0 :
                self.dataDump()
            else :
                self.dataRestore()



    def simulate(self,buildingName):
        rm2 = RoomsManager()

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

            if len(self.statusDict) == 0: self.dataRestore()

            roomSimulator = RoomSimulator(buildingName=buildingName, roomName=room,
                                              occupancyTimeRangeFrom=h,
                                              occupancyTimeRangeTo=hTo, roomTemperature=self.statusDict[room]["RoomTemp"],
                                              externalTemperature=self.statusDict[room]["ExtTemp"], weather=self.statusDict[room]["Weather"])

            self.saveSim(roomSimulator.start(),h,room)
            self.tempSimulator(room)
            self.humSimulator(room)
            self.powerSimulator(room)

            users = rm2.getUsers(room,buildingName)["users"]

            print self.buildingUsers
            self.scoresRestore()
            for user in users:
                if user["username"] in self.scores:
                    self.getScores(user["username"],room)
                    print str(user["username"]) + str(room)

            if len(self.statusDictControl)!= 0 :
                self.dataDump()
            else :
                self.dataRestore()

    def getScores(self,username,roomName):
        whyNotHappy = ""
        whyManagerNotHappy = ""
        youHappy = True
        managerHappy = True

        roomManager = RoomsManager()

        now = datetime.datetime.now()
        h = now.hour

        if h > 18 or h < 8:
            if "LIGHT" in self.statusAction[roomName]:
                if self.statusAction[roomName]["LIGHT"] != "ON":
                    youHappy = False
                    whyNotHappy = whyNotHappy + "The Light are OFF and outside is very dark <br/>"
            else:
                youHappy = False
                whyNotHappy = whyNotHappy + "The Light are OFF and outside is very dark <br/>"

        if h > 8 and h < 18:
            if "Office" in (roomManager.getInfo(roomName, "CSE"))["description"]:
                if "COMPUTER" in self.statusAction[roomName]:
                    if self.statusAction[roomName]["COMPUTER"] != "ON":
                        youHappy = False
                        whyNotHappy = whyNotHappy + "The PC is off during working time!(8-18) <br/>"
                else:
                    youHappy = False
                    whyNotHappy = whyNotHappy + "The PC is off during working time!(8-18) <br/>"

        #hvac + window open
        if "TEMPERATURE" in self.statusAction[roomName] and "WINDOWS" in self.statusAction[roomName]:
            if self.statusAction[roomName]["WINDOWS"] == "OPEN":
                managerHappy = False
                whyManagerNotHappy = whyManagerNotHappy + "Did you open the window with the HVAC active? <br/>"

        #not sunny + light off
        if self.statusDict[roomName]["Weather"]!="sunny":
            if "LIGHT" in self.statusAction[roomName]:
                if self.statusAction[roomName]["LIGHT"] != "ON":
                    youHappy = False
                    whyNotHappy = whyNotHappy + "The Light are OFF and there is no sun outside <br/>"
            else:
                youHappy = False
                whyNotHappy = whyNotHappy + "The Light are OFF and there is no sun outside <br/>"

        #hum > 30
        if  self.statusDictControl[roomName]["Hum"] > 30 :
            youHappy = False
            whyNotHappy = whyNotHappy + "Humidity over 30% <br/>"

        #room temp < 64 o > 72
        if  self.statusDictControl[roomName]["RoomTemp"] < 64 and self.statusDictControl[roomName]["RoomTemp"]> 72 :
            youHappy = False
            whyNotHappy = whyNotHappy + "Room Temperature over 72F or under 64F <br/>"


        if self.statusDictControl[roomName]["Power"] > 2000 :
            managerHappy = False
            whyManagerNotHappy = whyManagerNotHappy + "The power consumption is over 2000 W <br/>"

        if managerHappy:
            self.scores[username]+=1
        else:
            self.scores[username]-=1

        if youHappy:
            self.scores[username]+=1
        else:
            self.scores[username]-=1
        print self.scores[username]

        self.roomHappiness[roomName]["you"] = youHappy
        self.roomHappiness[roomName]["manager"] = managerHappy

        self.roomHappiness[roomName]["whyYou"] = whyNotHappy
        self.roomHappiness[roomName]["whyManager"] = whyManagerNotHappy

        self.scoresDump()

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
                            if room["buildingName"] == "CSE":
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
                    ranking = sorted(self.scores.items(), key=operator.itemgetter(1),reverse=True)
                    for item in ranking:
                        message += str(item[0]) + " " + str(item[1]) + "\n"
                    notificationManager.sendNotificationByEmail(userUuid,"Building Summary",message)

    def changeWeather(self):
        temp = random.randrange(55,68,1)
        weather = random.randrange(1,3,1)
        if weather == 1:
            w = "sunny"
        if weather == 2:
            w = "cloudy"
        if weather == 3:
            w = "rainy"
        for room in self.roomList:
            self.statusDict[room]["Weather"] = w
            self.statusDictControl[room]["Weather"] = w
            self.statusDict[room]["ExtTemp"] = str(temp)+"F"
            self.statusDictControl[room]["ExtTemp"] = temp


    def mailServiceExec(self,scheduler = None):
        if scheduler is None:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(21600, 1, self.mailServiceExec, ([scheduler]))
            scheduler.run()
        if scheduler is not None:
            scheduler.enter(21600, 1, self.mailServiceExec, ([scheduler]))

        #self.sendSummaryByEmail()
        self.changeWeather()

    def threadExec(self,buildingName,scheduler = None):

        if scheduler is None:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(1, 1, self.threadExec, ([buildingName, scheduler]))
            scheduler.run()
        if scheduler is not None:
            scheduler.enter(1800, 1, self.threadExec, ([buildingName, scheduler]))

        self.simulate(buildingName)

    def dataDump(self):
        dataDumpFolder = "tools/gameData/"
        if not os.path.exists(dataDumpFolder): os.makedirs(dataDumpFolder)

        statusDictControlFile = "statusDictControlFile.json"
        statusDictControlFilePath = (dataDumpFolder + "/" + statusDictControlFile).replace("//", "/")
        os.remove(statusDictControlFilePath) if os.path.exists(statusDictControlFilePath) else None

        outputStatus = open(statusDictControlFilePath,'wb')
        json.dump(self.statusDictControl,outputStatus)

        outputStatus.close()



    def dataRestore(self):
        dataRestoreFolder = "tools/gameData/"
        if not os.path.exists(dataRestoreFolder): return False

        statusDictControlFile = "statusDictControlFile.json"
        statusDictControlFilePath = (dataRestoreFolder + "/" + statusDictControlFile).replace("//", "/")
        if not os.path.exists(statusDictControlFilePath): return False

        inputStatus = open(statusDictControlFilePath,'rb')
        self.statusDictControl = json.load(inputStatus)

        inputStatus.close()
        print self.statusDictControl
        for room in self.roomList:
            valuesDict = {"ExtTemp": str(self.statusDictControl[room]["ExtTemp"]) + "F", "RoomTemp":str(self.statusDictControl[room]["RoomTemp"]) + "F", "Hum":str(self.statusDictControl[room]["Hum"]) + "%","Weather":self.statusDictControl[room]["Weather"],"Power": self.statusDictControl[room]["Power"]}
            self.statusDict[room] = valuesDict

        return True


    def scoresDump(self):
        dataDumpFolder = "tools/gameData/"
        if not os.path.exists(dataDumpFolder): os.makedirs(dataDumpFolder)

        scoresFile = "scoresFile.json"
        scoresFilePath = (dataDumpFolder + "/" + scoresFile).replace("//", "/")
        os.remove(scoresFilePath) if os.path.exists(scoresFilePath) else None

        outputScores = open(scoresFilePath,'wb')
        json.dump(self.scores,outputScores)

        outputScores.close()


    def scoresRestore(self):
        dataRestoreFolder = "tools/gameData/"
        if not os.path.exists(dataRestoreFolder): return False

        scoresFile = "scoresFile.json"
        scoresFilePath = (dataRestoreFolder + "/" + scoresFile).replace("//", "/")
        if not os.path.exists(scoresFilePath): return False

        with open(scoresFilePath,'rb') as inputScores:
            self.scores = json.load(inputScores)

        return True

    def humidityDump(self):
        dataDumpFolder = "tools/gameData/"
        if not os.path.exists(dataDumpFolder): os.makedirs(dataDumpFolder)

        humFile = "humidityFile.json"
        humFilePath = (dataDumpFolder + "/" + humFile).replace("//", "/")
        os.remove(humFilePath) if os.path.exists(humFilePath) else None

        outputHum = open(humFilePath,'wb')
        json.dump(self.targetHum,outputHum)

        outputHum.close()


    def tempDump(self):
        dataDumpFolder = "tools/gameData/"
        if not os.path.exists(dataDumpFolder): os.makedirs(dataDumpFolder)

        tempFile = "tempFile.json"
        tempFilePath = (dataDumpFolder + "/" + tempFile).replace("//", "/")
        os.remove(tempFilePath) if os.path.exists(tempFilePath) else None

        outputTemp = open(tempFilePath,'wb')
        json.dump(self.targetTemp,outputTemp)

        outputTemp.close()


    def humidityRestore(self):
        dataRestoreFolder = "tools/gameData/"
        if not os.path.exists(dataRestoreFolder): return False

        humFile = "humidityFile.json"
        humFilePath = (dataRestoreFolder + "/" + humFile).replace("//", "/")
        if not os.path.exists(humFilePath): return False

        with open(humFilePath,'rb') as inputHum:
            self.targetHum = json.load(inputHum)



        return True

    def tempRestore(self):
        dataRestoreFolder = "tools/gameData/"
        if not os.path.exists(dataRestoreFolder): return False

        tempFile = "tempFile.json"
        tempFilePath = (dataRestoreFolder + "/" + tempFile).replace("//", "/")
        if not os.path.exists(tempFilePath): return False

        with open(tempFilePath,'rb') as inputTemp:
            self.targetTemp = json.load(inputTemp)
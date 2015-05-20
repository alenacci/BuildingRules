import os
import math
import urllib2
import datetime
import time
from flask import json
import matplotlib.pyplot as plt

from app.backend.controller.buildingsManager import BuildingsManager

__author__ = 'jacopo'

#Internal temperature simulator (PSEUDOCODE)

#If windows opened (do not consider HVAC)
    #Check for extTemp
    #Set initial extTemp as a delta from extTemp
    #If extTemp == intTemp
        #same temp
    #If extTemp != intTemp
        #recalculate each hour based on the updated extTemp, behave like RC with tau = 5 to reach extTemp

#If windows closed (do not consider extTemp)
    #If intTemp < setTemp
        #behave like RC with tau = 5
    #If intTemp > setTemp
        #behave like RC discharging tau = 5
def start():


    username = "admin"

    buildingsManager = BuildingsManager()
    buildings = buildingsManager.getAllBuildings()

    internalTempDict = {}

    restReadDone = False
    try:
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=Milano,it&units=Imperial'
        response = urllib2.urlopen(url).read()
        restReadDone = True
    except Exception as e:
        print(e.message)

    if restReadDone:

        if not os.path.exists("tools/simulation/ThorSim/"):
            os.makedirs("tools/simulation/ThorSim/")


        out_file = open("tools/simulation/ThorSim/weather.json","w")
        out_file.write(response)
        out_file.close()


    for building in buildings["buildings"]:
        rooms = buildingsManager.getRooms(building["buildingName"],username)
        for room in rooms["rooms"]:
            print room
            roomData = fetchDataFromJSON(room["roomName"])
            if roomData != "" :
                if not os.path.exists("tools/simulation/ThorSim/"+building["buildingName"]+"/"+room["roomName"]): os.makedirs("tools/simulation/ThorSim/"+building["buildingName"]+"/"+room["roomName"])

                #INIT
                intTemp = 55 #init temp
                windowsStatus = "CLOSE"
                hvacStatus = False
                hvacTemp = 0

                transientExtTemp = 0.0
                deltaTWindow = 0.0
                transientDurationWindow = 0
                transientExpCoefWindow=0.0


                transientHvacTemp = 0.0
                deltaTHvac = 0.0
                transientDurationHvac = 0
                transientExpCoefHvac=0.0

                intTempGraphValues = []
                extTempGraphValues = []
                hvacTempGraphValues = []
                xValues = []
                hourGraph = 0

                extTemp = 40
                firstOpened = True
                firstClosed = True
                day = 1
                for simulation in roomData.items():
                    print simulation
                    for hour in range(0,24,1):
                        temp = getExtTemp(day,hour)
                        if temp != "":
                            extTemp = int(temp)

                        for category in simulation[1]["simulation"].items() :
                            for ruleDetail in category[1]:
                                if float(ruleDetail["from"].replace(":",".")) <= hour <= float(ruleDetail["to"].replace(":",".")) :

                                    if category[0] == "WINDOWS":
                                        windowsStatus = ruleDetail["status"]
                                    if category[0] == "TEMPERATURE":
                                        temperatures = ruleDetail["status"].strip().split("-")
                                        newTemps = []
                                        newTemps.append(temperatures[0].replace("F",""))
                                        newTemps.append(temperatures[1].replace("F",""))
                                        #facciamo la media delle 2 temp nel set?
                                        hvacTemp = int(newTemps[0])
                                        hvacStatus = True



                        if windowsStatus == "OPEN":
                            if extTemp != intTemp:
                                if transientExtTemp != extTemp:
                                    transientExtTemp = extTemp
                                    deltaTWindow = (extTemp - intTemp)
                                    transientExpCoefWindow = float(abs(deltaTWindow))/float(max(extTemp,intTemp))
                                    transientDurationWindow = 1
                                else:
                                    transientDurationWindow +=1
                                intTemp = extTemp - (deltaTWindow)*math.exp(-transientExpCoefWindow*transientDurationWindow)

                                transientHvacTemp = 0.0

                                #recalculate each hour based on the updated extTemp, behave like RC with tau = 5 to reach extTemp
                        elif hvacStatus:
                            if intTemp != hvacTemp:
                                if transientHvacTemp != hvacTemp:
                                    transientHvacTemp = hvacTemp
                                    deltaTHvac = (hvacTemp - intTemp)
                                    transientExpCoefHvac = float(abs(deltaTHvac))/float(max(hvacTemp,intTemp))
                                    transientDurationHvac = 1


                                else:
                                    transientDurationHvac +=1

                                intTemp = hvacTemp - (deltaTHvac)*math.exp(-transientExpCoefHvac*transientDurationHvac)

                                transientExtTemp = 0.0

                        saveData = {}
                        saveData["windows"] = windowsStatus
                        saveData["hvac"] = hvacTemp
                        saveData["intTemp"] = intTemp
                        saveData["extTemp"] = extTemp
                        internalTempDict[hourGraph + hour] = saveData
                        xValues.append(hourGraph + hour)
                        intTempGraphValues.append(intTemp)
                        extTempGraphValues.append(extTemp)
                        hvacTempGraphValues.append(hvacTemp)

                        if (hourGraph + hour != 0) :
                            if internalTempDict[hourGraph + hour - 1]["windows"] != internalTempDict[hourGraph + hour]["windows"] :


                                if internalTempDict[hourGraph + hour - 1]["windows"] == "OPEN" :
                                    if firstOpened :
                                        firstOpened = False
                                        plt.axvline(x=hourGraph + hour-1,linestyle="dotted",color="red",label ="Windows Closed")
                                    else :
                                        plt.axvline(x=hourGraph + hour-1,linestyle="dotted",color="red")

                                else :
                                    if firstClosed :
                                        firstClosed= False
                                        plt.axvline(x=hourGraph + hour-1,linestyle="dotted",color="green",label ="Windows Opened")
                                    else:
                                        plt.axvline(x=hourGraph + hour-1,linestyle="dotted",color="green")

                    hourGraph += 24
                    day += 1
                plt.plot(xValues,intTempGraphValues,label="intTemp")
                plt.plot(xValues,extTempGraphValues,label="extTemp")
                plt.plot(xValues,hvacTempGraphValues,label="hvacTemp",linestyle = "dashed")
                plt.legend(loc="lower right")
                plt.title(building["buildingName"]+" - "+room["roomName"])
                plt.xlabel("Time [h]")
                plt.ylabel("Temperature [F]")
                plt.savefig("tools/simulation/ThorSim/"+building["buildingName"]+"/"+room["roomName"]+ "/ThorSimResultsGraph.png")
                plt.close()
                jsonResultsPath = "tools/simulation/ThorSim/"+building["buildingName"]+"/"+room["roomName"]+ "/ThorSimResultsData.json"
                outputResults = open(jsonResultsPath,'wb')
                json.dump(internalTempDict,outputResults)






def fetchDataFromJSON(roomName):
    if os.path.exists("tools/simulation/results/" + roomName + ".json"):
        in_file = open("tools/simulation/results/" + roomName + ".json","r")
        in_data = json.load(in_file)
        return in_data
    else:
        return ""


def getExtTemp(day,hour):
    if os.path.exists("tools/simulation/ThorSim/weather.json"):
        in_file = open("tools/simulation/ThorSim/weather.json","r")
        in_data = json.load(in_file)
        for record in in_data["list"]:
            if record["dt_txt"] == strTime(day,hour):
                return record["main"]["temp"]
        return ""

def strTime(day,hour):
    currentDateTime = datetime.datetime.today() + datetime.timedelta(days=day)
    currentDateTime = currentDateTime.strftime("%Y-%m-%d")
    strHour = str(hour)
    if len(strHour) == 1:
        strHour = "0" + str(hour)

    currentDateTimeStr = str(currentDateTime)

    currentDateTimeStr += " " + strHour + ":00:00"

    return currentDateTimeStr
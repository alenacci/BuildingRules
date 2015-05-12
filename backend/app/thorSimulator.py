import os
from flask import json

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
    windowsStatus = ""
    hvacTemp = 0

    for building in buildings["buildings"]:
        rooms = buildingsManager.getRooms(building["buildingName"],username)
        for room in rooms["rooms"]:
            print room
            roomData = fetchDataFromJSON(room["roomName"])
            if roomData != "" :
                if not os.path.exists("tools/simulation/ThorSim/"+building["buildingName"]+"/"+room["roomName"]): os.makedirs("tools/simulation/ThorSim/"+building["buildingName"]+"/"+room["roomName"])

                #INIT
                intTemp = 0 #init temp
                windowsStatus = "CLOSE"
                for simulation in roomData.items():
                    for hour in range(0,24,1):
                        extTemp = getExtTemp(building["buildingName"], hour)

                        for category in simulation[1]["simulation"].items() :
                            print category
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
                                        hvacTemp = newTemps[0]



                        if windowsStatus == "OPEN":

                            print("implement windows opened")

                            if extTemp != intTemp:
                                print("implement inttemp != exttemp")
                                #recalculate each hour based on the updated extTemp, behave like RC with tau = 5 to reach extTemp

                        else:
                            print("implement windows closed")
                            if intTemp < hvacTemp:
                                print("implement inttemp < hvactemp")
                                #behave like RC with tau = 5
                            if intTemp > hvacTemp:
                                print("implement inttemp > hvactemp")
                                #behave like RC discharging tau = 5


                        internalTempDict[hour] = intTemp
                #saveJSON internalTemp




def fetchDataFromJSON(roomName):
    if os.path.exists("tools/simulation/results/" + roomName + ".json"):
        in_file = open("tools/simulation/results/" + roomName + ".json","r")
        in_data = json.load(in_file)
        return in_data
    else:
        return ""


def getExtTemp(buildingName, hour):
    return 15
import sys
import time
import datetime
import copy
import os
import string
import random

from app.backend.commons.inputDataChecker import checkData
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.actionExecutor import ActionExecutor

class RoomSimulator:

	def __init__(self, buildingName = None, roomName = None, occupancyTimeRangeFrom = None, occupancyTimeRangeTo = None, roomTemperature = None, externalTemperature = None, weather = None):
		
		checkData(locals())

		self.buildingName = buildingName
		self.roomName = roomName
		self.occupancyTimeRangeFrom = occupancyTimeRangeFrom
		self.occupancyTimeRangeTo = occupancyTimeRangeTo
		self.roomTemperature = roomTemperature
		self.externalTemperature = externalTemperature
		self.weather = weather


	def _getCurrentOccupancy(self, currentTimeMinutes):

		occupancyTimeRangeMinuteFrom = self._getTimeInMinutes(self.occupancyTimeRangeFrom)
		occupancyTimeRangeMinuteTo = self._getTimeInMinutes(self.occupancyTimeRangeTo)


		if currentTimeMinutes >= occupancyTimeRangeMinuteFrom and currentTimeMinutes <= occupancyTimeRangeMinuteTo:
			return True
		else:
			return False


	def start(self):

		simulationBufferFolder = "tools/simulation/"
		if not os.path.exists(simulationBufferFolder): os.makedirs(simulationBufferFolder)
		simulationBufferFileName = self.__addPrefixToFileName(self.buildingName + "_" + self.roomName + ".sim")
		simulationBufferFilePath = (simulationBufferFolder + "/" + simulationBufferFileName).replace("//", "/")
		os.remove(simulationBufferFilePath) if os.path.exists(simulationBufferFilePath) else None

		for hour in range(0,24):
			for minute in range(0,60,60):

				h = str(hour) if len(str(hour)) == 2 else "0" + str(hour)
				m = str(minute) if len(str(minute)) == 2 else "0" + str(minute)
				currentTime = h + ":" + m
				currentTimeMinutes = hour * 60 + minute

				simulationParameters = {}
		 		simulationParameters['roomTemperature'] = self.roomTemperature
		 		simulationParameters['occupancy'] = self._getCurrentOccupancy(currentTimeMinutes)
		 		simulationParameters['day'] = self._getCurrentDay()
		 		simulationParameters['date'] = self._getCurrentDate()
		 		simulationParameters['weather'] = self.weather
		 		simulationParameters['externalTemperature'] = self.externalTemperature
		 		simulationParameters['time'] = currentTime
		 		simulationParameters['resultsBufferFile'] = simulationBufferFilePath

				roomFilter = [ {'buildingName' : self.buildingName, 'roomName' : self.roomName} ]

				actionExecutor = ActionExecutor(simulationParameters = simulationParameters, roomFilter = roomFilter)
				actionExecutor.start()



		f = open(simulationBufferFilePath)
		lines = f.readlines()
		f.close()

		os.remove(simulationBufferFilePath) if os.path.exists(simulationBufferFilePath) else None

		actionTargets = set()
		actionTargetsRecordsNumber = {}
		timeRecords = []

		for line in lines:
			
			record = line.replace("\n","").split(";")	
			timeRecords.append(record)
			actionTargets.add(record[2])
			if record[2] not in actionTargetsRecordsNumber.keys(): actionTargetsRecordsNumber[record[2]] = 0
			actionTargetsRecordsNumber[record[2]] += 1

		gantt = {}
		for target in actionTargets:
			gantt[target] = []




		for target in actionTargets:

			lastTargetStatus = None
			lastTargetStatusStartTime = '00:00'
			targetCounter = 0

			for record in timeRecords:

				if record[2] == target:		

					if lastTargetStatus != record[3]:
						
						if lastTargetStatus != None:
							gantt[target].append({"from": lastTargetStatusStartTime, "to" : record[1], "status" : lastTargetStatus})
						
						lastTargetStatus = record[3]
						lastTargetStatusStartTime = record[1]

					targetCounter += 1

					if targetCounter == actionTargetsRecordsNumber[target]:
						gantt[target].append({"from": "00.00", "to" : record[1], "status" : record[3]})					

		print gantt
					
		return {"simulation" : gantt}

	def _getCurrentDate(self):
		return str(time.strftime("%d/%m"))

	def _getCurrentDay(self):

		currentDayInt = datetime.datetime.today().weekday()	

		if currentDayInt == 0: return "Monday"
		if currentDayInt == 1: return "Tuesday"
		if currentDayInt == 2: return "Wednesday"
		if currentDayInt == 3: return "Thursday"
		if currentDayInt == 4: return "Friday"
		if currentDayInt == 5: return "Saturday"
		if currentDayInt == 6: return "Sunday"


	def _getTimeInMinutes(self, timeString):

		plainTime = timeString.replace("AM", "").replace("PM", "").replace("am", "").replace("pm", "").strip().replace(":",".")

		hour = int(plainTime[:plainTime.find(".")])
		minute = int(plainTime[plainTime.find(".")+1:])

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




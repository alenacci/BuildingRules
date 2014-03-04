import sys
import time
import datetime
import copy

from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.actionExecutor import ActionExecutor

class RoomSimulator:

	def __init__(self, buildingName = None, roomName = None, occupancyTimeRangeFrom = None, occupancyTimeRangeTo = None, temperature = None, weather = None):
		
		self.buildingName = buildingName
		self.roomName = roomName
		self.occupancyTimeRangeFrom = occupancyTimeRangeFrom
		self.occupancyTimeRangeTo = occupancyTimeRangeTo
		self.temperature = temperature
		self.weather = weather


	def _getCurrentOccupancy(self, currentTimeMinutes):

		occupancyTimeRangeMinuteFrom = self._getTimeInMinutes(self.occupancyTimeRangeFrom)
		occupancyTimeRangeMinuteTo = self._getTimeInMinutes(self.occupancyTimeRangeTo)


		if currentTimeMinutes >= occupancyTimeRangeMinuteFrom and currentTimeMinutes <= occupancyTimeRangeMinuteTo:
			return True
		else:
			return False


	def startSimulation(self):

		for hour in range(0,24):
			for minute in range(0,60,60):

				h = str(hour) if len(str(hour)) == 2 else "0" + str(hour)
				m = str(minute) if len(str(minute)) == 2 else "0" + str(minute)
				currentTime = h + ":" + m
				currentTimeMinutes = hour * 60 + minute

				print currentTime,
				print " " + str(currentTimeMinutes), 
				print " " + str(self._getCurrentOccupancy(currentTimeMinutes))


				simulationParameters = {}
		 		simulationParameters['temperature'] = self.temperature
		 		simulationParameters['occupancy'] = self._getCurrentOccupancy(currentTimeMinutes)
		 		simulationParameters['day'] = self._getCurrentDay()
		 		simulationParameters['date'] = self._getCurrentDate()
		 		simulationParameters['weather'] = self.weather
		 		simulationParameters['time'] = currentTime
		 		simulationParameters['resultsBufferFile'] = "simul_tmp.txt"

				roomFilter = [ {'buildingName' : self.buildingName, 'roomName' : self.roomName} ]

				actionExecutor = ActionExecutor(simulationParameters = simulationParameters, roomFilter = roomFilter)
				actionExecutor.start()

	def getSimulationResults(self):
		pass

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


	def __str__(self):
		return "RoomSimulator: "		




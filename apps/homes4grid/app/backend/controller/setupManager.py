############################################################
#
# BuildingRules Project 
# Politecnico di Milano
# Author: Alessandro A. Nacci
#
# This code is confidential
# Milan, March 2014
#
############################################################

import sys
import time
import datetime
import copy
import json


from app.backend.commons.errors import *
from app.backend.model.settings import Settings
from app.backend.model.appliance import Appliance
from app.backend.model.appliancesNetwork import AppliancesNetwork

class SetupManager:

	def __init__(self):
		pass

	def getTimeslotsGanttByFamilyProfile(self, familyProfile, applianceName):
		path = "tools/default_timeslots/" + familyProfile + ".json"
		
		try:
			in_file = open(path,"r")
			jsonStr = in_file.read()
			in_file.close()
		except:
			raise DefaultTimeSlotReadError("Impossible to read the default time slot for the " + familyProfile + " family profile")


		gantts = json.loads(jsonStr)

		return gantts[applianceName]


	def initializeNetwork(self, familyProfile):

		validValues = ["single_men", "single_women", "friends_group", "couple", "couple_child"]

		if familyProfile not in validValues:
			raise NotValidFamilyProfileError("The required family profile is not valid")

		settings =  Settings()
		settings.set("familyProfile", familyProfile)

		applianceListStr = settings.get("applianceList")
		applianceList = applianceListStr.replace(" ", "").split(",")

		for applianceName in applianceList:
			
			label = applianceName.replace("_", " ")
			#label[0] = label[0].upper()

			appliance = Appliance(
					name = applianceName,
					label = label,
					timeslots = self.getTimeslotsGanttByFamilyProfile(familyProfile, applianceName)
			)

			appliance.store()

	def __str__(self):
		return "SetupManager: "		



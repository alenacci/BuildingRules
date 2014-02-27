import sys
import os
import sys
import subprocess
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from database import Database
import rest

sessionKey = None
userUuid = None
username = "admin"
password = "brulesAdmin2014"



def execProcess(cmd):

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()

	return output


def getUserActionOnRule(action):
	currentFile = "../../frontend/logs/api_requests.log"
	cmd = "cat " + currentFile + " | grep rules | grep " + action + " | grep -c API_REQUEST"
	output = execProcess(cmd).replace("\n","").strip()
	return "Number of total " + action + " request: " + output


def getUserActionOnRulePerDay(action):

	result = []

	for day in getExperimentDaysList():
		currentFile = "../../frontend/logs/api_requests.log"
		cmd = "cat " + currentFile + ' | grep rules | grep ' + action + ' | grep API_REQUEST | grep -c "> ' + day + '"'
		output = execProcess(cmd).replace("\n","").strip()
		result.append( "Number of total " + action + " request on " + day + ": " + output )

	return result


def getExperimentDaysList():
	daysList = []

	firstDay = date(2014,02,1)
	today = date.today()
	deltaDays = (today - firstDay).days

	currentDay = firstDay
	for i in range(1, deltaDays+2):
		daysList.append(currentDay.strftime("%Y-%m-%d"))
		currentDay += timedelta(days=1)

	return daysList


def getRoomList():

	query = "SELECT DISTINCT room_name FROM `rooms`"

	database = Database()
	database.open()
	queryResult = database.executeReadQuery(query)
	database.close()

	roomList = []
	
	for record in queryResult:
		roomList.append(record[0])

	return roomList

def getRuleList():

	query = "SELECT * FROM `rules`"

	database = Database()
	database.open()
	queryResult = database.executeReadQuery(query)
	database.close()


	ruleList = []
	
	for record in queryResult:
		recDict = {}
		recDict["id"] = record[0]
		recDict["priority"] = record[1]
		recDict["category"] = record[2]
		recDict["buildingName"] = record[3]
		recDict["groupId"] = record[4]
		recDict["roomName"] = record[5]
		recDict["authorUuid"] = record[6]
		recDict["antecedent"] = record[7]
		recDict["consequent"] = record[8]
		recDict["enabled"] = record[9]
		recDict["deleted"] = record[10]
		recDict["creationTimestamp"] = record[11] 
		recDict["lastEditTimestamp"] = record[12]

		ruleList.append(recDict)

	return ruleList


def getTimeConflictData(recordFilter):

	if recordFilter == "ALL":
		query = "SELECT * FROM `logs` WHERE `logMessage` LIKE '%RoomRuleVerification%'"
	elif recordFilter == "SUCCESS":
		query = "SELECT * FROM `logs` WHERE `logMessage` LIKE '%RoomRuleVerification [SUCCESS]%'"
	elif recordFilter == "FAILED":
		query = "SELECT * FROM `logs` WHERE `logMessage` LIKE '%RoomRuleVerification [FAILED]%'"
	else:
		print "error filter"
		sys.exit()

	database = Database()
	database.open()
	queryResult = database.executeReadQuery(query)
	database.close()


	ruleVerificationStats_cardinality = {}
	ruleVerificationStats_avg = {}
	ruleVerificationStats_sum = {}
	ruleVerificationStats_max = {}
	ruleVerificationStats_min = {}

	for record in queryResult:
		
		numberOfRulesStrIndex = record[2].find("#rules=") + len("#rules=")
		numberOfRules = record[2][numberOfRulesStrIndex:].split("-")[0].strip()

		millisecondsStrIndex = record[2].find("opTimeMilliseconds:") + len("opTimeMilliseconds:")
		milliseconds = record[2][millisecondsStrIndex:].strip()

		numberOfRules = int(numberOfRules)
		milliseconds = int(milliseconds)

		if numberOfRules not in ruleVerificationStats_cardinality.keys(): ruleVerificationStats_cardinality[numberOfRules] = 0
		ruleVerificationStats_cardinality[numberOfRules] += 1

		if numberOfRules not in ruleVerificationStats_sum.keys(): ruleVerificationStats_sum[numberOfRules] = 0
		ruleVerificationStats_sum[numberOfRules] += milliseconds

		if numberOfRules not in ruleVerificationStats_max.keys(): ruleVerificationStats_max[numberOfRules] = 0
		if milliseconds > ruleVerificationStats_max[numberOfRules]: ruleVerificationStats_max[numberOfRules] = milliseconds
		
		if numberOfRules not in ruleVerificationStats_min.keys(): ruleVerificationStats_min[numberOfRules] = sys.maxint
		if milliseconds < ruleVerificationStats_min[numberOfRules]: ruleVerificationStats_min[numberOfRules] = milliseconds


	# Computing average
	for numberOfRules in ruleVerificationStats_cardinality.keys():
		ruleVerificationStats_avg[numberOfRules] = ruleVerificationStats_sum[numberOfRules] / ruleVerificationStats_cardinality[numberOfRules]

	return ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min


def getRuleAntecedentTriggerInfo(ruleAntecedent):
	global sessionKey
	global userUuid

	response = rest.request("/api/tools/triggers/translate", {
			'sessionKey' : sessionKey,
			'userUuid' : userUuid,
			'antecedent' : ruleAntecedent
			})

	return response["triggers"]


def getRuleConsequentActionInfo(ruleConsequent):
	global sessionKey
	global userUuid

	response = rest.request("/api/tools/actions/translate", {
			'sessionKey' : sessionKey,
			'userUuid' : userUuid,
			'consequent' : ruleConsequent
			})

	return response["action"]


def login():

	global sessionKey
	global userUuid
	global username
	global password

	response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})
	sessionKey = response["sessionKey"]
	userUuid = response["userUuid"]


###################################################################################################
###################################################################################################
###################################################################################################


login()

triggerCategoryCounter = {}
triggerNameCounter = {}

actionCategoryCounter = {}
actionNameCounter = {}

triggerActionCategoryCounter = {}
triggerActionNameCounter = {}

for rule in getRuleList():


	#print getRuleAntecedentTriggerInfo(rule["antecedent"])
	print getRuleConsequentActionInfo(rule["consequent"])
	raw_input()


sys.exit()


#GETTING DATA ABOUT THE CONFLICT DETECTION (BOTH SUCCESS AND FAIL)
ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min = getTimeConflictData("ALL")
ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min = getTimeConflictData("SUCCESS")
ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min = getTimeConflictData("FAILED")


#GETTING DATA ABOUT THE USERS REQUEST (ADD EDIT RULE)
print getUserActionOnRule("add")
print getUserActionOnRule("edit")
print getUserActionOnRule("delete")
print getUserActionOnRule("disable")
print getUserActionOnRule("enable")


print getUserActionOnRulePerDay("add")
print getUserActionOnRulePerDay("edit")
print getUserActionOnRulePerDay("delete")
print getUserActionOnRulePerDay("disable")
print getUserActionOnRulePerDay("enable")


import sys
import os
import sys
import subprocess
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from database import Database

def execProcess(cmd):

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()

	return output



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


###################################################################################################
###################################################################################################
###################################################################################################

#GETTING DATA ABOUT THE CONFLICT DETECTION (BOTH SUCCESS AND FAIL)



ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min = getTimeConflictData("ALL")
print ruleVerificationStats_avg


sys.exit()

# Total add requests
currentFile = "../../frontend/logs/api_requests.log"
cmd = "cat " + currentFile + " | grep rules | grep add | grep -c API_REQUEST"
output = execProcess(cmd).replace("\n","").strip()
print "Number of total add request: " + output


# Total edit requests
currentFile = "../../frontend/logs/api_requests.log"
cmd = "cat " + currentFile + " | grep rules | grep edit | grep -c API_REQUEST"
output = execProcess(cmd).replace("\n","").strip()
print "Number of total edit request: " + output

# Total add request per day
for day in getExperimentDaysList():
	currentFile = "../../frontend/logs/api_requests.log"
	cmd = "cat " + currentFile + ' | grep rules | grep add | grep API_REQUEST | grep -c "> ' + day + '"'
	output = execProcess(cmd).replace("\n","").strip()
	print "Number of total add request on " + day + ": " + output

# Total edit request per day
for day in getExperimentDaysList():
	currentFile = "../../frontend/logs/api_requests.log"
	cmd = "cat " + currentFile + ' | grep rules | grep edit | grep API_REQUEST | grep -c "> ' + day + '"'
	output = execProcess(cmd).replace("\n","").strip()
	print "Number of total edit request on " + day + ": " + output



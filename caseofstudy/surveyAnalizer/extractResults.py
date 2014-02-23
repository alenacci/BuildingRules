import json
import os
import sys

def write(fileName, line):
	f = open(fileName,'a')
	f.write(line + "\n") 
	f.close() 

def writeAggregate(label, value):
	line = label + ";" + str(value)
	write("aggregate.csv", line)

def writeDetail(line):
	write("detail.csv", line)


if os.path.exists("aggregate.csv"): os.remove("aggregate.csv")
if os.path.exists("detail.csv"): os.remove("detail.csv")


f = open("results.txt")
lines = f.readlines()
f.close()


values = {}

for line in lines:
	splittedLine = line.split(";")

	lineNumber = int(splittedLine[0].strip())
	timestamp = splittedLine[1]
	content = splittedLine[2].replace("'",'"').replace("set(","").replace(")","")
	content = json.loads(content)

	if lineNumber == 0:
		for key, value in content.iteritems():

			if key == "consequentStats":
				for k,v in value.iteritems():
					writeAggregate(k,v) 

			elif key == "antecedentStats":
				for k,v in value.iteritems():
					writeAggregate(k,v)
			else:
				writeAggregate(key,value)
	else:
		
		if content["occupants"] not in values.keys():
			values[content["occupants"]] = {}
			values[content["occupants"]]["cardinality"] = 0
			values[content["occupants"]]["logicalConflicts"] = 0
			values[content["occupants"]]["runtimeConflicts"] = 0
			values[content["occupants"]]["duplicatedRules"] = 0

		values[content["occupants"]]["cardinality"] += 1
		values[content["occupants"]]["logicalConflicts"] += content["logicalConflicts"] 
		values[content["occupants"]]["runtimeConflicts"] += content["runtimeConflicts"] 
		values[content["occupants"]]["duplicatedRules"] += content["duplicatedRules"]


maxVal = {}
minVal = {}

for occupants in values.keys():

	if not occupants in minVal.keys():
		minVal[occupants] = {}
		for k in values[occupants].keys():
			if k != "cardinality" :  minVal[occupants][k] = sys.maxint
	
	if not occupants in maxVal.keys():
		maxVal[occupants] = {}
		for k in values[occupants].keys():
			if k != "cardinality" : maxVal[occupants][k] = 0

	for k in values[occupants].keys():
		if k != "cardinality" :
			if values[occupants][k] < minVal[occupants][k] : minVal[occupants][k] = values[occupants][k]
			if values[occupants][k] > maxVal[occupants][k] : maxVal[occupants][k] = values[occupants][k]

writeDetail("occupants;cardinality;max_logicalConflicts;min_logicalConflicts;avg_logicalConflicts;max_runtimeConflicts;min_runtimeConflicts;avg_runtimeConflicts;max_duplicatedRules;min_duplicatedRules;avg_duplicatedRules;")
for occupants in values.keys():

	for k in values[occupants].keys():
		values[occupants][k] /= values[occupants]["cardinality"]

	line = str(occupants) + ";" + str(values[occupants]["cardinality"])  + ";"
	line += str(maxVal[occupants]["logicalConflicts"])  + ";" + str(minVal[occupants]["logicalConflicts"]) + ";" + str(values[occupants]["logicalConflicts"])  + ";"
	line += str(maxVal[occupants]["runtimeConflicts"])  + ";" + str(minVal[occupants]["runtimeConflicts"]) + ";" + str(values[occupants]["runtimeConflicts"])  + ";"
	line += str(maxVal[occupants]["duplicatedRules"])  + ";" + str(minVal[occupants]["duplicatedRules"]) + ";" + str(values[occupants]["duplicatedRules"])  + ";"

	writeDetail(line)





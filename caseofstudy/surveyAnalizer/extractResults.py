import json
import os


def write(fileName, line):
	f = open(fileName,'a')
	f.write(line + "\n") 
	f.close() 

def writeAggregate(label, value):
	line = label + ";" + str(value)
	write("aggregate.csv", line)

def writeAverage(line):
	write("average.csv", line)


if os.path.exists("aggregate.csv"): os.remove("aggregate.csv")
if os.path.exists("average.csv"): os.remove("average.csv")


f = open("results.txt")
lines = f.readlines()
f.close()


average = {}

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
		
		if content["occupants"] not in average.keys():
			average[content["occupants"]] = {}
			average[content["occupants"]]["cardinality"] = 0
			average[content["occupants"]]["logicalConflicts"] = 0
			average[content["occupants"]]["runtimeConflicts"] = 0
			average[content["occupants"]]["duplicatedRules"] = 0

		average[content["occupants"]]["cardinality"] += 1
		average[content["occupants"]]["logicalConflicts"] += content["logicalConflicts"] 
		average[content["occupants"]]["runtimeConflicts"] += content["runtimeConflicts"] 
		average[content["occupants"]]["duplicatedRules"] += content["duplicatedRules"]




writeAverage("occupants;cardinality;logicalConflicts;runtimeConflicts;duplicatedRules")
for occupants in average.keys():
	average[occupants]["logicalConflicts"] /= average[occupants]["cardinality"] 
	average[occupants]["runtimeConflicts"] /= average[occupants]["cardinality"] 
	average[occupants]["duplicatedRules"] /= average[occupants]["cardinality"] 

	writeAverage( str(occupants) + ";" + str(average[occupants]["cardinality"])  + ";" + str(average[occupants]["logicalConflicts"]) + ";" + str(average[occupants]["runtimeConflicts"]) + ";" +  str(average[occupants]["duplicatedRules"]))
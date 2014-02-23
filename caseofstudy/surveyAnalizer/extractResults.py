import json


def write(fileName, line):
	f = open(fileName,'a')
	f.write(line + "\n") 
	f.close() 

def writeAggregate(label, value):
	line = label + ";" + str(value)
	write("aggregate.csv", line)

f = open("results.txt")
lines = f.readlines()
f.close()


for line in lines:
	splittedLine = line.split(";")

	lineNumber = int(splittedLine[0].strip())
	timestamp = splittedLine[1]
	content = json.loads(splittedLine[2])


	if lineNumber == 0:
		for key, value in content.iteritems():

			if key == "consequentStats":
				print "ciao"
				for k,v in value.iteritems():
					writeAggregate(k,v)
			elif key == "antecedentStats":
				for k,v in value.iteritems():
					writeAggregate(k,v)
			else:
				writeAggregate(key,value)


	
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


from app import app

def writeSimulationLog(simulationParameters, actionTargetName, actionTargetStatus):

	line = simulationParameters["date"] + ";" + simulationParameters["time"] + ";" + actionTargetName + ";" + str(actionTargetStatus)
	open(simulationParameters["resultsBufferFile"],"a").write( line + "\n")
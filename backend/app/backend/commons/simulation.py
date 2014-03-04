from app import app

def writeSimulationLog(simulationParameters, actionTargetName, actionTargetStatus):

	line = simulationParameters["date"] + ";" + simulationParameters["time"] + ";" + actionTargetName + ";" + str(actionTargetStatus)
	open(simulationParameters["resultsBufferFile"],"a").write( line + "\n")
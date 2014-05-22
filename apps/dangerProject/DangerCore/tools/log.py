import time

def log_event(name):
	logmessage = ""
	t = time.time()
	if name:
		logmessage = str(t) + ": " + name
	else:
		logmessage = str(t)

	with open("log.txt", "a") as logfile:
		logfile.write(logmessage + "\n")
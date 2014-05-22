#!flask/bin/python
from threading import Thread
import os

print ("RUN.py executed")

def startWebServer():
	os.system("python runWebServer.py io")

def startDangerLogic():
	os.system("python runDangerLogic.py")





### MAIN STARTS HERE

#dangerLogicThread = Thread(target = startDangerLogic)
#dangerLogicThread.start()

webServerThread = Thread(target = startWebServer)
webServerThread.start()

#dangerLogicThread.join()
webServerThread.join()
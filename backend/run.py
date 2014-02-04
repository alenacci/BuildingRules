#!venv/bin/python
import sys
import os
import time
from threading import Thread
import datetime
import subprocess

__BACKEND_SERVER_PORT = "5003"

def startWebServer():
	os.system("python runWebServer.py")

def startDeamon():
	os.system("python runDeamon.py")

def startWeatherService():
	os.system("python runWeatherService.py")


### MAIN STARTS HERE

webServerThread = Thread(target = startWebServer)
webServerThread.start()

weatherServiceThread = Thread(target = startWeatherService)
weatherServiceThread.start()

deamonThread = Thread(target = startDeamon)
deamonThread.start()



webServerThread.join()
deamonThread.join()
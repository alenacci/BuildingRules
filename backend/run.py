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

def startGraphDeamon():
   os.system("python runGraphDeamon.py")

def startRealTimeExecutor():
    os.system("python runRealTimeExecutor.py")

def startWeatherService():
    os.system("python runWeatherService.py")

def startMailService():
    os.system("python runMailService.py")

def startDatabaseDumper():
    os.system("python runDatabaseDumper.py")

def startThorSimulator():
    os.system("python runThorSimulator.py")

def startOptimizationDaemon():
    os.system("python runOptimizationDaemon")


### MAIN STARTS HERE

webServerThread = Thread(target = startWebServer)
webServerThread.start()

weatherServiceThread = Thread(target = startWeatherService)
weatherServiceThread.start()

mailServiceThread = Thread(target = startMailService)
#mailServiceThread.start()

databaseDumperThread = Thread(target = startDatabaseDumper)
#databaseDumperThread.start()

deamonThread = Thread(target = startDeamon)
deamonThread.start()

# graphDeamonThread = Thread(target = startGraphDeamon)
# graphDeamonThread.start()

# thorSimulatorThread = Thread(target = startThorSimulator())
# thorSimulatorThread.start()

optimizationDaemon = Thread(target = startOptimizationDaemon)
optimizationDaemon.start()

realTimeThread = Thread(target = startRealTimeExecutor())
realTimeThread.start()

webServerThread.join()
deamonThread.join()
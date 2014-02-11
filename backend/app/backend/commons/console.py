from app import app
import sys
import time
import datetime
import json
import logging


def flash(message, color = None):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	message = "BRules> " + str(st) + " > " + str(message)

	logging.basicConfig(filename='logs/deamon.log')
	logging.getLogger().addHandler(logging.StreamHandler())
	logging.info(message)
	logging.exception("")

	if color:
		if color == "red":
			message = '\033[1;31m' + message + '\033[1;m'
		elif color == "green":
			message =  '\033[1;32m' + message + '\033[1;m'
		elif color == "blue":
			message =  '\033[1;34m' + message + '\033[1;m'			
		elif color == "yellow":
			message =  '\033[1;33m' + message + '\033[1;m'									
		elif color == "gray":
			message =  '\033[1;30m' + message + '\033[1;m'			

	print message


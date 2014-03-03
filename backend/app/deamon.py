import sys
import time
import datetime
import copy

from app.backend.commons.console import flash
from app.backend.controller.actionExecutor import ActionExecutor


def start():
	flash("BuildingRules Deamon is active...")

	actionExecutor = ActionExecutor()

	while(1):
		try:
			actionExecutor.executeActions()
		except Exception as e:
			import logging
			logging.basicConfig(filename='logs/deamon.log')
			logging.getLogger().addHandler(logging.StreamHandler())			
			logging.exception("")
			flash(e.message)

		time.sleep(600)
		


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


import time

from app.backend.commons.console import flash
from app.backend.controller.actionExecutor import ActionExecutor


def start():
	flash("BuildingRules Deamon is active...")

	actionExecutor = ActionExecutor(buildingFilter="CSE")

	while(1):
		try:
			actionExecutor.start()
		except Exception as e:
			import logging
			logging.basicConfig(filename='logs/deamon.log')
			logging.getLogger().addHandler(logging.StreamHandler())
			logging.exception("")
			flash(e.message)

		time.sleep(600)
		


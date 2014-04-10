import sys
import time
import datetime
import copy

from app.backend.commons.console import flash
from app.backend.controller.actionExecutor import ActionExecutor

class RealTimeExecutor:

	requestUpdate = False

	@staticmethod
	def valueChanged():
		requestUpdate = True

	@staticmethod
	def start():
		actionExecutor = ActionExecutor()

		while(1):
			if RealTimeExecutor.requestUpdate:
				requestUpdate = False

				try:
					actionExecutor.start(skipRealTime=False)
				except Exception as e:
					import logging
					logging.basicConfig(filename='logs/deamon.log')
					logging.getLogger().addHandler(logging.StreamHandler())
					logging.exception("")
					flash(e.message)
			else:
				flash("no realtime update requested", "blue")
			time.sleep(10)



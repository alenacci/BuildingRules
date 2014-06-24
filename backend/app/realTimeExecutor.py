import sys
import time
import datetime
import copy
from multiprocessing.connection import Listener

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


		address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
		listener = Listener(address)


		while(1):
			conn = listener.accept()
			print 'connection accepted from', listener.last_accepted
			msg = conn.recv()
			print 'RECEIVED ' +  msg
			if msg == 'update':
				RealTimeExecutor.requestUpdate = True
				conn.close()



			if RealTimeExecutor.requestUpdate:
				RealTimeExecutor.requestUpdate = False

				try:
					actionExecutor.start(only_real_time_triggers=True)
				except Exception as e:
					import logging
					logging.basicConfig(filename='logs/deamon.log')
					logging.getLogger().addHandler(logging.StreamHandler())
					logging.exception("")
					flash(e.message)
			else:
				flash("no realtime update requested", "blue")


		listener.close()



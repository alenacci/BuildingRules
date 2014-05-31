from module import Module
from behaviors.actions.moveAction import MoveAction
from renderer import Renderer
import pygame
import urllib2
import threading
import concurrent
import json
from pygame import Surface
import math

class DangerModule(Module):

	ALARM_EFFECT_FREQUENCY = 2

	def __init__(self, simulator):

		Module.__init__(self, simulator)

		#start pooling
		t = threading.Timer(2, self._read_notifications_from_danger_core)
		t.daemon = True
		t.start()

		self.last_timestamp = 0
		self.alarm = False
		self.start_alarm_time = 0


		self.surface = pygame.Surface((Renderer.WINDOW_WIDTH, Renderer.WINDOW_HEIGHT))
		red = [255,0,0]
		self.surface.fill(red,[0, 0,Renderer.WINDOW_WIDTH, Renderer.WINDOW_HEIGHT])

	def after_populate(self, agents):
		#give a name to each user
		for i, a in enumerate(agents):
			a.danger_name = "user" + str(i);


	def _read_notifications_from_danger_core(self):

		try:
			message = {
				'timestamp': str(self.last_timestamp)
			}

			req = urllib2.Request('http://localhost:2001/api/user/get_notifications')
			req.add_header('Content-Type', 'application/json')

			response = json.loads(urllib2.urlopen(req, json.dumps(message)).read())


			if response['new_notifications'] == 'True':
				for notification in response['notifications']:

					self.last_timestamp = int(notification['timestamp'])
					if notification['type'] == 'danger':
						self._trigger_alarm()
		except Exception:
			print "unable to connect to danger core"

		#restart pooling
		t = threading.Timer(2, self._read_notifications_from_danger_core)
		t.daemon = True
		t.start()

	def _trigger_alarm(self):
		self.alarm = True


	def render_foreground(self, window):
		if self.alarm:
			t = self.simulator.time
			alpha = abs(math.sin( (t - self.start_alarm_time) * DangerModule.ALARM_EFFECT_FREQUENCY ) ) * 100
			self.surface.set_alpha(alpha)

			window.blit(self.surface, (0, 0) )
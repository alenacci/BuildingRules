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
from triggers.trigger import Trigger
from behaviors.escape_behavior import EscapeBehavior
import random

class DangerModule(Module):

	ALARM_EFFECT_FREQUENCY = 2.3
	IP = "192.168.43.172"

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

		alarm_notification = False

		try:

			message = {
				'timestamp': str(self.last_timestamp)
			}

			req = urllib2.Request('http://'+ self.IP + ':2001/api/user/get_notifications')
			req.add_header('Content-Type', 'application/json')

			response = json.loads(urllib2.urlopen(req, json.dumps(message)).read())

			#print response

			if response['new_notifications'] == 'True':
				for notification in response['notifications']:

					self.last_timestamp = int(notification['timestamp'])
					if notification['type'] == 'danger':
						alarm_notification = True
		except Exception:
			#print "unable to connect to danger core"
			pass

		if alarm_notification:
			self._trigger_alarm()

		#restart pooling
		t = threading.Timer(2, self._read_notifications_from_danger_core)
		t.daemon = True
		t.start()

	def _trigger_alarm(self):
		self.alarm = True
		self.simulator.trigger_manager.fire_trigger(Trigger("alarm"))
		print "ALARM"
		self._escape()

	def _escape(self):

		#ESCAPE
		for a in self.simulator.agents:

			#schedule escape
			room = self.simulator.building.room_at_position(a.p)

			#if room is None the agent is already out of the building
			if room is not None:

				##ESCAPE TIME ROOMS
				if hasattr(room, "escape_wait_time"):
					wait_time = room.escape_wait_time
					wait_time += random.random()*3
				else:
					room.escape_wait_time = 2 * random.random() * 10
					wait_time = room.escape_wait_time

				t = threading.Timer(wait_time, self.start_escape,args=[a])
				t.setDaemon(True)
				t.start()


	def start_escape(self,agent):
		if not type(agent.behavior) is EscapeBehavior:
			agent.behavior.stop()
			beh = EscapeBehavior()
			beh.escape_regions = [ [(37, 30), (46, 0)],
									[(46, 19), (51, 0)],
									[(53, 7),  (63, 0)]  ]
			agent.behavior = beh

			beh.start()

	def render_foreground(self, window):
		if self.alarm:
			t = self.simulator.time
			alpha = abs(math.sin( (t - self.start_alarm_time) * DangerModule.ALARM_EFFECT_FREQUENCY ) ) * 100
			self.surface.set_alpha(alpha)

			window.blit(self.surface, (0, 0) )
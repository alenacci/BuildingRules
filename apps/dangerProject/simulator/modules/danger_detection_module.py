from module import Module
from behaviors.actions.moveAction import MoveAction
from renderer import Renderer
from danger_module import DangerModule
import pygame
import urllib2
import json
import concurrent

class DangerDetectionModule(Module):



	def __init__(self,simulator):
		Module.__init__(self,simulator)


	def after_populate(self, agents):
		for a in agents:
			a.on_room_changed.connect(self._on_room_changed, identifyObserved=True)
			self._send_bulletin(a)


	def _on_room_changed(self, agent, room):
		self._send_bulletin(agent)


	def _send_bulletin(self, agent):
		"""send a bulletin to the virtual sensor"""
		message = {
        	'id': agent.id,
			'room'	: agent.current_room.id
		}

		req = urllib2.Request('http://' + DangerModule.IP + ':2001/api/register_user')
		req.add_header('Content-Type', 'application/json')

		try:
			response = urllib2.urlopen(req, json.dumps(message))
		except Exception, e:
			print str(e) + "unable to connect to dangerCore (depot)"

	def _on_alarm_triggered(self, trigger):
		self.disabled = True
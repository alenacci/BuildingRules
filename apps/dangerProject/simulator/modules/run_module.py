from module import Module
from behaviors.actions.moveAction import MoveAction
from danger_module import DangerModule
from renderer import Renderer
import pygame
import urllib2
import json
import concurrent

class RunModule(Module):

	RUNNING_THRESHOLD = 3.5
	MOV_ICON_SIZE = 16

	def __init__(self,simulator):
		Module.__init__(self,simulator)
		self.agent_move_image = pygame.image.load("./res/mov.png")
		self.agent_move_image = pygame.transform.scale(self.agent_move_image, (RunModule.MOV_ICON_SIZE, RunModule.MOV_ICON_SIZE))
		self.background_executor = concurrent.futures.ThreadPoolExecutor(5)
		self.simulator.trigger_manager.subscribe("alarm", self._on_alarm_triggered)
		self.disabled = False

	def after_populate(self, agents):
		for a in agents:
			a.on_action_changed.connect(self._on_action_changed, identifyObserved=True)
			a.is_running = False

	def _on_action_changed(self, agent, action):

		if self.disabled:
			return

		if isinstance(action, MoveAction) and action.speed >= RunModule.RUNNING_THRESHOLD and not agent.is_running:
			agent.is_running = True
			self.background_executor.submit(self._send_bulletin, agent)
		else:
			agent.is_running = False

	def render_agent(self, window, agent):
		"""Draw around the circle of the agent an icon for showing that it is running"""

		if self.disabled:
			return

		if agent.is_running:
			tr = (RunModule.MOV_ICON_SIZE - Renderer.AGENT_SIZE)/2
			dest_x = agent.x * Renderer.SIZE_X - tr + Renderer.OFFSET_X
			dest_y = agent.y * Renderer.SIZE_Y - tr + Renderer.OFFSET_Y
			window.blit(self.agent_move_image, (dest_x, dest_y) )


	def _send_bulletin(self, agent):
		"""send a bulletin to the virtual sensor"""
		message = {
        	'user': agent.danger_name,
			'state' : 'running',
			'buildings' : 'simulator',
			'room'	: str(agent.current_room.id)
		}

		req = urllib2.Request('http://' + DangerModule.IP + ':2560/api/notify_run')
		req.add_header('Content-Type', 'application/json')

		try:
			response = urllib2.urlopen(req, json.dumps(message))
		except Exception:
			print "unable to connect to virtual sensor"

	def _on_alarm_triggered(self, trigger):
		self.disabled = True
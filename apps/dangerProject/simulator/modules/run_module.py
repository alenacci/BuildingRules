from module import Module
from behaviors.actions.moveAction import MoveAction
from renderer import Renderer
import pygame


class RunModule(Module):

	RUNNING_THRESHOLD = 3.5
	MOV_ICON_SIZE = 16

	def __init__(self,simulator):
		Module.__init__(self,simulator)
		self.agent_move_image = pygame.image.load("./res/mov.png")
		self.agent_move_image = pygame.transform.scale(self.agent_move_image, (RunModule.MOV_ICON_SIZE, RunModule.MOV_ICON_SIZE))

	def after_populate(self, agents):
		for a in agents:
			a.on_action_changed.connect(self._on_action_changed, identifyObserved=True)
			a.is_running = False

	def _on_action_changed(self, agent, action):
		if isinstance(action, MoveAction) and action.speed >= RunModule.RUNNING_THRESHOLD:
			agent.is_running = True
		else:
			agent.is_running = False

	def render_agent(self, window, agent):
		"""Draw around the circle of the agent an icon for showing that it is running"""

		if agent.is_running:
			tr = (RunModule.MOV_ICON_SIZE - Renderer.AGENT_SIZE)/2
			dest_x = agent.x * Renderer.SIZE_X - tr + Renderer.OFFSET_X
			dest_y = agent.y * Renderer.SIZE_Y - tr + Renderer.OFFSET_Y
			window.blit(self.agent_move_image, (dest_x, dest_y) )
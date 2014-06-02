from module import Module
import pygame
import renderer
from commons.point import Point
import simulator
from behaviors.fire_behavior import FireBehavior

class Fire:
	def __init__(self, room, position):
		self.room = room
		self.position = position

	def __str__(self):
		return "fire"

class FireModule(Module):


	def __init__(self,simulator):
		Module.__init__(self,simulator)
		self.fire_image = pygame.image.load("./res/fire/fire.png")

		#SUBSCRIBE to all the triggers named "fire"
		self.simulator.trigger_manager.subscribe("fire", self._on_fire_trigger)
		self.fires = []

	def render_building(self, window):
		for f in self.fires:
			pos = renderer.Renderer.convert_point(f.position)
			pos[0] -= 10
			pos[1] -= 40
			window.blit(self.fire_image, pos )

	def _on_fire_trigger(self,trigger):
		fire = Fire(trigger.room, trigger.position)
		self.fires.append(fire)
		for a in simulator.sim.agents:
			# TODO __eq__
			if str(a.current_room) == str(trigger.room):
				a.behavior = FireBehavior()
				a.behavior.start(fire)

	def update_agent(self, agent, time):
		Module.update_agent(self, agent, time)

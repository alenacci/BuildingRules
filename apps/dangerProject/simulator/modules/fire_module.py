from module import Module
import pygame
import renderer
from commons.point import Point

class Fire:
	pass


class FireModule(Module):


	def __init__(self,simulator):
		Module.__init__(self,simulator)
		self.fire_image = pygame.image.load("./res/fire/fire.png")
		self.simulator.trigger_manager.subscribe("fire", self._on_fire_trigger )
		self.fires = []

	def render_building(self, window):
		for f in self.fires:
			pos = renderer.Renderer.convert_point(f.pos)
			pos[0] -= 10
			pos[1] -= 40
			window.blit(self.fire_image, pos )

	def _on_fire_trigger(self,trigger):
		room_id = trigger.room_id
		room = self.simulator.building.rooms[room_id]
		pos = room.random_position()
		fire = Fire()
		fire.room = room
		fire.pos = pos
		self.fires.append(fire)

	def update_agent(self, agent, time):
		if agent.p == 
		Module.update_agent(self, agent, time)
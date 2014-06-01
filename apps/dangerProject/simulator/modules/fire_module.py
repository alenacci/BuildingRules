from module import Module
import pygame
import renderer
from commons.point import Point
import simulator

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
		self.simulator.trigger_manager.subscribe("fire", self._on_fire_trigger )
		self.fires = []

	def render_building(self, window):
		for f in self.fires:
			pos = renderer.Renderer.convert_point(f.position)
			pos[0] -= 10
			pos[1] -= 40
			window.blit(self.fire_image, pos )

	def _on_fire_trigger(self,trigger):
		room_id = trigger.room_id
		room = self.simulator.building.rooms[room_id]
		pos = room.random_position()
		fire = Fire(room, pos)
		self.fires.append(fire)

	def update_agent(self, agent, time):
		if len(self.fires) > 0:
			if str(simulator.sim.building.room_at_position(agent.p)) == str((self.fires[len(self.fires)-1]).room):
				agent.alert = self.fires[len(self.fires)-1]

		Module.update_agent(self, agent, time)
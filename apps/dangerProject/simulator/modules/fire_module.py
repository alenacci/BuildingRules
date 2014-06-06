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
				if not type(a.behavior) is FireBehavior:
					a.behavior.stop()
					a.behavior = FireBehavior()
					a.behavior.escape_regions = [ [(37, 30), (46, 0)],
										[(46, 19), (51, 0)],
										[(53, 7),  (63, 0)]  ]
					a.behavior.start(fire)
		#make the fire not walkable
		for i in range(-1,3):
			for j in range(-1, 3):
				# if i,j<gridsize
				self.simulator.building.grid.tiles[int(trigger.position.x)+i][int(trigger.position.y)+j].walkable = False


	def update_agent(self, agent, time):
		Module.update_agent(self, agent, time)

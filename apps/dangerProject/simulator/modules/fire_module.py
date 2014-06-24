from module import Module
import pygame
import renderer
from commons.point import Point
import simulator
from behaviors.fire_behavior import FireBehavior
from behaviors.escape_behavior import EscapeBehavior
import random

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

	def after_populate(self, agents):
		for a in agents:
			a.on_room_changed.connect(self._on_room_changed, identifyObserved=True)

	def render_building(self, window):
		for f in self.fires:
			pos = renderer.Renderer.convert_point(f.position)
			pos[0] -= 10
			pos[1] -= 40
			window.blit(self.fire_image, pos )

	def _on_fire_trigger(self, trigger):

		room = self.simulator.building.rooms[trigger.room_id]
		###XXX PSEUDO RANDOM
		tile = random.Random(500).choice(room.tiles)
		position = Point(tile.x,tile.y)
		fire = Fire(room, position)

		self.fires.append(fire)

		#Escape
		for a in simulator.sim.agents:

			if a.current_room is not None and a.current_room == room:
				if not type(a.behavior) is FireBehavior:
					self._escape_agent(a,fire)

		#make the fire not walkable
		for i in range(-1,3):
			for j in range(-1, 3):
				# if i,j<gridsize
				self.simulator.building.grid.tiles[int(position.x)+i][int(position.y)+j].walkable = False



	def update_agent(self, agent, time):
		Module.update_agent(self, agent, time)

	def _escape_agent(self,a,fire):
		a.behavior.stop()
		a.behavior = FireBehavior()
		a.behavior.escape_regions = [ [(37, 30), (46, 0)],
										[(46, 19), (51, 0)],
										[(53, 7),  (63, 0)]  ]
		a.behavior.start(fire)


	def _on_room_changed(self, agent, room):

		"""When an agent enter in a room, if there is a fire he escapes"""
		for f in self.fires:
			if f.room == room:

				if not type(agent.behavior) is EscapeBehavior:
					agent.behavior.stop()
					beh = EscapeBehavior()
					beh.escape_regions = [ [(37, 30), (46, 0)],
											[(46, 19), (51, 0)],
											[(53, 7),  (63, 0)]  ]
					agent.behavior = beh
					beh.start()

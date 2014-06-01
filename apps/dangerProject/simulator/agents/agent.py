from commons.point import Point
import utils
from behaviors.actions.moveAction import MoveAction
from utils import event
import simulator
import copy

class Agent(object):

	agents_count = 0

	def __init__(self):
		self.p = Point(0,0)
		self._current_action = None
		self._behavior = None
		self.current_tile = None
		#set an id based on the agents count
		self.id = Agent.agents_count
		Agent.agents_count += 1

		self._update_current_tile()

	def setPosition(self,p):
		self.p = p.dup()
		self._update_current_tile()

	@property
	def x(self):
		return self.p.x

	@x.setter
	def x(self, x):
		self.p.x = x
		self._update_current_tile()

	@property
	def y(self):
		return self.p.y

	@y.setter
	def y(self, y):
		self.p.y = y
		self._update_current_tile()

	@property
	def current_action(self):
		return self._current_action

	@current_action.setter
	def current_action(self, action):
		action.agent = self
		self._current_action = action
		self.on_action_changed(action)

	@property
	def behavior(self):
		return self._behavior

	#Assign a behavior to our agent
	@behavior.setter
	def behavior(self, behavior):
		self._behavior = behavior
		self.behavior.setAgent(self)
		self.on_behavior_changed(behavior)

	@property
	def current_room(self):
		if self.current_tile:
			return self.current_tile.room

	#update the tile where the agent is placed
	#and the corresponding room
	def _update_current_tile(self):
		grid = simulator.sim.building.grid
		tile = grid.tiles[int(self.x)][int(self.y)]
		room = tile.room

		if self.current_room != room:
			if self.current_room:
				self.current_room.agents.remove(self)
			if room:
				room.agents.append(self)


		if self.current_tile is None or not self.current_tile == tile:

			if self.current_tile:
				self.current_tile.agents.remove(self)
			if tile:
				tile.agents.append(self)

			self.current_tile = tile

			others = (copy.copy(tile.agents))
			others.remove(self)
			if len(others) > 0:
				self.on_meet_others(others)

	""" events """
	@event
	def on_action_changed(self, action):
		pass

	@event
	def on_behavior_changed(self, behavior):
		pass

	@event
	def on_meet_others(self, others):
		"""called when the agent is in the same tile with others"""
		pass

	""" update functions """

	def update(self):
		if self.current_action:
			self.current_action.update()

		if self.behavior:
			self.behavior.update()

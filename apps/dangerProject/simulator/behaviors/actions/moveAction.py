from action import Action
import simulator
from behaviors.path import *
from utils import *


class NoPathToTargetDestination(Exception):
	pass


class MoveAction(Action):
	def __init__(self,agent,sPoint,ePoint):
		Action.__init__(self,agent)
		self.s_point = sPoint
		self.e_point = ePoint
		self.duration = 1

	def start(self):
		#get the tile where the start and end are
		s_x = int(self.s_point.x)
		s_y = int(self.s_point.y)
		e_x = int(self.e_point.x)
		e_y = int(self.e_point.y)

		self.path = findPath(simulator.sim.grid,s_x,s_y,e_x,e_y)

		if not self.path:
			raise NoPathToTargetDestination()

		#then, substitute the start and the end point
		self.path.start = self.s_point
		self.path.end = self.e_point


		Action.start(self)

	def update(self):
		if not self.active:
			return

		cur_time = worldTime()
		progress = (cur_time - self.start_time) / self.duration

		if progress > 1:
			self.end()

		cur_position = self.path.getPositionAtPercentage(progress)

		self.agent.setPosition(cur_position)

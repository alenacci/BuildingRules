from action import Action
import simulator
from behaviors.path import *
from utils import *
import random

class NoPathToTargetDestination(Exception):
	pass


class MoveAction(Action):
	def __init__(self,agent,sPoint,ePoint):
		Action.__init__(self,agent)
		self.s_point = sPoint
		self.e_point = ePoint
		self.duration = None
		self.speed = 2 + random.random()*5
		self.path = None


	def start(self):
		#get the tile where the start and end are placed
		s_x = int(self.s_point.x)
		s_y = int(self.s_point.y)
		e_x = int(self.e_point.x)
		e_y = int(self.e_point.y)

		#launch the a-star computation on another thread
		self.path_future = simulator.sim.background_executor.submit(findPath, simulator.sim.building.grid, s_x, s_y, e_x, e_y)
		self.path_future.add_done_callback(self._on_path_computation_ended)
		self.wait = True


	def _on_path_computation_ended(self, path_future):
		self.wait = False
		self.path = path_future.result()
		if not self.path or self.path.length == 0:
			#raise NoPathToTargetDestination()
			#TODO right? maybe length = 0 should be dealt in different way
			self.end()

		#then, substitute the start and the end point
		self.path.start = self.s_point
		self.path.end = self.e_point
		self.path.recomputeDistances()
		self.duration = self.path.length / self.speed
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

	def __str__(self):
		return "moveAction"
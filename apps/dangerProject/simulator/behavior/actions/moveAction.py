from action import Action
import simulator
from behavior.path import *
from utils.worldTime import *

class MoveAction(Action):
	def __init__(self,agent,sPoint,ePoint):
		Action.__init__(self,agent)
		self.s_point = sPoint
		self.e_point = ePoint
		self.duration = 3.0

	def start(self):
		Action.start(self)
		self.path = findPath(simulator.sim.grid, int(self.s_point.x),int(self.s_point.y),int(self.e_point.x),int(self.e_point.y))


	def update(self):
		if not self.active:
			return

		cur_time = worldTime()
		progress = (cur_time - self.start_time) / self.duration

		if progress > 1:
			self.end()



		cur_position = self.path.getPositionAtPercentage(progress)
		print(cur_position)
		self.agent.setPosition(cur_position)

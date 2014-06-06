from action import Action
import simulator
from behaviors.path import *
from utils import *





class WaitAction(Action):
	def __init__(self,agent, time):
		Action.__init__(self,agent)
		self.duration = time

	def start(self):
		Action.start(self)

	def update(self):
		if not self.active:
			return

		cur_time = worldTime()
		progress = (cur_time - self.start_time) / self.duration

		if progress > 1:
			self.end()

	def __str__(self):
		return "waitAction"
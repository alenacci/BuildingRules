import commons
import behaviors.actions as actions
from math import sqrt
from task import Task
import random
import simulator

class FireTask(Task):

	def __init__(self, agent, fire):
		Task.__init__(self, agent)
		self.fire = fire
		self.counter = 0


		# MOVE AWAY
		new_pos = self.agent.current_room.random_position()
		while new_pos.dist(self.fire.position) < 5 :
			new_pos = self.fire.room.random_position()
		self.move_away = actions.MoveAction(agent,new_pos)
		self.actions.append(self.move_away)


	def start(self):
		Task.start(self)

	def on_action_ended(self, action):
		# SHAKING before escaping
		if self.counter < 8:
			pos = self.agent.p
			if self.counter%2 == 0:
				shake = actions.MoveAction(self.agent,commons.Point(pos.x+1, pos.y), speed = 8)
			else:
				shake = actions.MoveAction(self.agent,commons.Point(pos.x-1, pos.y), speed = 8)
			self.actions.append(shake)
			self.counter += 1
		Task.on_action_ended(self, action)


	def __str__(self):
		return "FireTask"
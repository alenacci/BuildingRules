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


		# MOVE AWAY
		new_pos = self.agent.current_room.random_position()
		while new_pos.dist(self.fire.position) < 5 :
			new_pos = self.fire.room.random_position()
		self.move_away = actions.MoveAction(agent,new_pos)
		self.actions.append(self.move_away)

		# SHAKING
		for i in range (1, 10):
			if i%2 == 0:
				pos = new_pos
			else:
				pos = commons.Point(new_pos.x + 4, new_pos.y)
		shake = actions.MoveAction(agent,pos)
		self.actions.append(shake)


	def start(self):
		Task.start(self)

	def on_action_ended(self, action):
		Task.on_action_ended(self, action)


	def __str__(self):
		return "FireTask"
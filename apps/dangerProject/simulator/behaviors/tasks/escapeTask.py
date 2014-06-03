import commons
import behaviors.actions as actions
from task import Task
import random
import simulator
from commons.point import Point


class EscapeTask(Task):
	def __init__(self, agent, region):
		Task.__init__(self, agent)

		x = region[0][0] + (region[1][0]-region[0][0])*random.random()
		y = region[0][1] + (region[1][1]-region[0][1])*random.random()

		self.escape_point = Point(x, y)

		#Wait before escaping
		self.actions.append(actions.WaitAction(agent, random.random()*1))

		#Escape action
		speed = 3 + random.random()*4
		escape_action = actions.MoveAction(agent, self.escape_point, speed)
		self.actions.append(escape_action)



		#Wait forever afterward
		wait_forever = actions.WaitAction(agent, 10E3)
		self.actions.append(wait_forever)

	def start(self):
		Task.start(self)

	def on_action_ended(self, action):
		Task.on_action_ended(self, action)

	def __str__(self):
		return "escape task"
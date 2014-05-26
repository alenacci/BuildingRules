import commons
import behaviors.actions as actions
from task import Task
import random

class ToiletTask(Task):
	def __init__(self, agent):
		Task.__init__(self, agent)
		self.sPoint = commons.Point(15,15)

		# GO TO TOILET
		go_to_toilet = actions.MoveAction(agent,agent.p,commons.Point(21,54))
		self.actions.append(go_to_toilet)

		# PISS
		piss = actions.WaitAction(agent, random.randint(1,3))
		self.actions.append(piss)

		# RETURN TO WORK
		return_to_work = actions.MoveAction(agent, commons.Point(21,54), self.sPoint)
		self.actions.append(return_to_work)

	def start(self):
		Task.start(self)



	def __str__(self):
		return "goToToilet"
import commons
import behaviors.actions as actions
from task import Task
import random
import simulator

class ToiletTask(Task):
	def __init__(self, agent):
		Task.__init__(self, agent)
		self.sPoint = agent.p.dup()
		self.wait_for_free_toilet = None
		self.e_point = None

		# GO TO TOILET
		self.go_to_toilet = actions.MoveAction(agent,commons.Point(25,random.randint(51,55)))
		self.actions.append(self.go_to_toilet)

		# PISS
		self.piss = actions.WaitAction(agent, random.randint(1,3))
		self.actions.append(self.piss)

		# RETURN TO WORK
		return_to_work = actions.MoveAction(agent, self.sPoint)
		self.actions.append(return_to_work)

	def start(self):
		Task.start(self)

	def on_action_ended(self, action):
		if action == self.go_to_toilet or action == self.wait_for_free_toilet:
			self.toiletChoice()
		elif action == self.piss:
			self.chosen_toilet.free = True

		Task.on_action_ended(self,action)

	def toiletChoice(self):
		for toilet in simulator.sim.building.toilets:
			# if simulator.sim.building.grid.tiles[toiletY][toiletX].free():
			if toilet.free:
				toilet.free = False
				self.chosen_toilet = toilet
				self.e_point = commons.Point(toilet.X, toilet.Y)
				go_to_free_toilet = actions.MoveAction(self.agent,self.e_point)
				self.actions.insert(self.current_action+1, go_to_free_toilet)
				break
		if self.e_point == None:
			self.wait_for_free_toilet = actions.WaitAction(self.agent,1)
			self.actions.insert(self.current_action+1, self.wait_for_free_toilet)

	def __str__(self):
		return "goToToilet"
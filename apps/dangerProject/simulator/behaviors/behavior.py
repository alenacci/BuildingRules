import tasks.toiletTask
import commons
import random
import simulator

''' abstract base class for all behaviors'''
class Behavior:

	def __init__(self):
		self.agent = None
		self.task = None

	def setAgent(self, agent):
		self.agent = agent

	#XXX TEMP
	def start(self):
		import actions
		action = actions.MoveAction(self.agent,self.agent.p,commons.Point(10, 12))
		self.agent.current_action = action
		action.end.connect(self.onActionEnded, identifyObserved=True)
		action.start()

	def newAction(self):
		decision = random.random()

		if decision>0:
			self.toilet()
		elif decision>0.7:
			self.newTarget()
		else:
			self.wait()

	#XXX TEMP
	def newTarget(self):
		w = simulator.sim.building.grid.GRID_WIDTH
		h = simulator.sim.building.grid.GRID_HEIGHT
		randw = random.randint(0,w-1)
		randh = random.randint(0,h-1)
		import actions
		action = actions.MoveAction(self.agent,self.agent.p,commons.Point(randw, randh))
		self.agent.current_action = action
		action.end.connect(self.onActionEnded, True)
		try:
			action.start()
		except actions.NoPathToTargetDestination:
			action.end()

	def wait(self):
		import actions
		action = actions.WaitAction(self.agent, random.randint(1,10))
		self.agent.current_action = action
		action.end.connect(self.onActionEnded, True)
		action.start()

	def toilet(self):
		self.task = tasks.toiletTask.ToiletTask(self.agent)
		print str(self.task)
		self.task.start()


	def onActionEnded(self,action):
		print str(action)
		self.newAction()

import actions
import commons
import random
import simulator

''' abstract base class for all behaviors'''
class Behavior:

	def __init__(self):
		self.agent = None

	def setAgent(self, agent):
		self.agent = agent

	#XXX TEMP
	def newAction(self):
		action = actions.MoveAction(self.agent,commons.Point(10, 10),commons.Point(10, 12))
		self.agent.current_action = action
		action.end.connect(self.onActionEnded, identifyObserved=True)
		action.start()

	#XXX TEMP
	def newTarget(self):
		w = simulator.sim.grid.GRID_WIDTH
		h = simulator.sim.grid.GRID_HEIGHT
		randw = random.randint(0,w-1)
		randh = random.randint(0,h-1)
		action = actions.MoveAction(self.agent,self.agent.p,commons.Point(randw, randh))
		self.agent._current_action = action
		action.end.connect(self.onActionEnded, True)
		try:
			action.start()
		except actions.NoPathToTargetDestination:
			action.end()


	def onActionEnded(self,action):
		self.newTarget()

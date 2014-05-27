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
		self.newAction()
		import actions
		#action = actions.MoveAction(self.agent, self.agent.p, commons.Point(10, 12))
		#self.agent.current_action = action
		#action.end.connect(self.onActionEnded, identifyObserved=True)
		#action.start()

	def newAction(self):
		decision = random.random()
		###TODO messo a 1 per non far crashare
		if decision>1:
			self.toilet()
		elif decision>0.7:
			self.newTarget()
		else:
			self.wait()

	#XXX TEMP
	def newTarget(self):
		pos = None
		decision = random.random()
		room = None
		#is more likely to move in the same room
		if decision > 0.3:
			room = simulator.sim.building.room_at_position(self.agent.p)
		else:
			room = simulator.sim.building.random_room()

		pos = room.random_position()

		import actions
		action = actions.MoveAction(self.agent, self.agent.p, pos )
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
		#print str(action)
		self.newAction()

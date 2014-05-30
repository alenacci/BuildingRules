import tasks.toiletTask
import commons
import random
import simulator
import utils

''' abstract base class for all behaviors'''
class Behavior:

	def __init__(self):
		self.agent = None
		self.task = None

		self._next_noise_time = None

	def setAgent(self, agent):
		self.agent = agent

	#XXX TEMP
	def start(self):
		self.newAction()
		import actions
		#action = actions.MoveAction(self.agent,commons.Point(10, 12))
		#self.agent.current_action = action
		#action.end.connect(self.onActionEnded, identifyObserved=True)
		#action.start()


	def newAction(self):
		decision = random.random()
		if decision > 0.9:
			self.toilet()
		elif decision > 0.7:
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

		action = actions.MoveAction(self.agent, pos )
		self.agent.current_action = action
		action.end.connect(self.onActionEnded, True)
		try:
			#print str(action)
			action.start()
		except actions.NoPathToTargetDestination:
			action.end()

	def wait(self, wait_time = None):
		if wait_time == None:
			wait_time = random.randint(1,10)
		import actions
		action = actions.WaitAction(self.agent, wait_time)
		self.agent.current_action = action
		action.end.connect(self.onActionEnded, True)
		#print str(action) + str(wait_time)
		action.start()


	def toilet(self):
		self.task = tasks.toiletTask.ToiletTask(self.agent)
		self.task.end.connect(self.onActionEnded, True)
		#print str(self.task)
		self.task.start()

	def onActionEnded(self,action):
		#print str(action)
		self.newAction()



	def alert(self):
		print " ___________"
		print "| ALERT!!!! |"
		print "'''''''''''''"
		self.wait(100)



	def update(self, alert = None):
		"""Now is quite useless"""
		pass

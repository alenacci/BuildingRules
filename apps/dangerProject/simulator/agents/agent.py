from commons.point import Point


class Agent(object):

	agents_count = 0

	def __init__(self):
		self.p = Point(0,0)
		self._current_action = None
		self._behavior = None

		#set an id based on the agents count
		self.id = Agent.agents_count
		Agent.agents_count += 1

	def setPosition(self,p):
		self.p = p.dup()

	@property
	def x(self):
		return self.p.x

	@x.setter
	def x(self, x):
		self.p.x = x

	@property
	def y(self):
		return self.p.y

	@y.setter
	def y(self, y):
		self.p.y = y

	@property
	def current_action(self):
		return self._current_action

	@current_action.setter
	def current_action(self, action):
		action.agent = self
		self._current_action = action

	@property
	def behavior(self):
		return self._behavior

	#Assign a behavior to our agent
	@behavior.setter
	def behavior(self, behavior):
		self._behavior = behavior
		self.behavior.setAgent(self)

	def update(self):
		if self.current_action:
			self.current_action.update()
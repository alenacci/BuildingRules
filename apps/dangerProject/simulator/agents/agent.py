from commons.point import Point
import utils
from behaviors.actions.moveAction import MoveAction

class Agent(object):

	RUNNING_THRESHOLD = 3.5

	agents_count = 0

	def __init__(self):
		self.p = Point(0,0)
		self._current_action = None
		self._behavior = None

		self.loud_noise_start_time = None
		self.loud_noise_duration = None
		self.is_generating_noise = False

		self.is_running = False

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


	def generate_loud_noise(self, duration):
		self.loud_noise_duration = duration
		self.is_generating_noise = True
		self.loud_noise_start_time = utils.worldTime()

	def update(self):
		if self.current_action:
			self.current_action.update()

		if self.behavior:
			self.behavior.update()

		if self.is_generating_noise and \
						self.loud_noise_start_time + self.loud_noise_duration < utils.worldTime():
			self.is_generating_noise = False

		if isinstance(self.current_action, MoveAction) and self.current_action.speed >= Agent.RUNNING_THRESHOLD:
			self.is_running = True
		else:
			self.is_running = False
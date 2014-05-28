from utils import *
from utils.decorator import *
#base abstract action that can be performed
#from the agents
class Action:

	def __init__(self, agent):
		self.agent = agent
		self.active = False
		self.start_time = None
		# if the action is not active but is waiting
		# for something else, for instance for some
		# computation to be completed
		self.wait = False
		#self.end_signal = Signal()

	def start(self):
		self.start_time = worldTime()
		self.active = True


	#called when the action ends

	@event
	def end(self):
		self.active = False
		#self.end_signal.fire(self)

	def update(self):
		pass

	def __str__(self):
		return "base action"
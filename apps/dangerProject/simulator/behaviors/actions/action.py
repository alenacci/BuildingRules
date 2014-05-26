from utils import *
from utils.decorator import *
#base abstract action that can be performed
#from the agents
class Action:

	def __init__(self, agent):
		self.agent = agent
		self.active = False
		#self.end_signal = Signal()

	def start(self):
		self.active = True
		self.start_time = worldTime()

	#called when the action ends

	@event
	def end(self):
		self.active = False
		#self.end_signal.fire(self)

	def update(self):
		pass

	def __str__(self):
		return "base action"
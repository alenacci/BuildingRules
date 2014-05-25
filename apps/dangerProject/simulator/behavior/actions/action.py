from utils.worldTime import *
#base abstract action that can be performed
#from the agents
class Action:

	def __init__(self,agent):
		self.agent = agent
		self.active = False


	def start(self):
		self.active = True
		self.start_time = worldTime()

	#called when the action ends
	def end(self):
		self.active = False

	def update(self):
		pass
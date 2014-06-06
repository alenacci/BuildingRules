import utils
#base abstract action that can be performed
#from the agents
class Task:

	def __init__(self,agent):
		self.agent = agent
		self.active = False
		self.actions = []
		self.current_action = 0
		#self.end_signal = Signal()

	def start(self):
		self.active = True
		self.start_time = utils.worldTime()

		self.launch_action(self.actions[self.current_action])

	#called when the action ends

	@utils.event
	def end(self):
		self.active = False
		#self.end_signal.fire(self)

	def launch_action(self, action):
		action.end.connect(self.on_action_ended, True)
		self.agent.current_action = action
		action.start()

	def on_action_ended(self, action):
		if self.current_action < len(self.actions) - 1:
			self.next_action()
		else:
			self.end()

	def stop(self):
		if self.actions[self.current_action] is not None:
			self.actions[self.current_action].stop()

	def next_action(self):
			self.current_action += 1
			self.launch_action(self.actions[self.current_action])

	def __str__(self):
		return "base task"
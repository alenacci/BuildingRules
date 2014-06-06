

class TriggerManager(object):
	def __init__(self):
		self.subscribers = {}

	def subscribe(self, trigger_name, callback):
		if self.subscribers.has_key(trigger_name):
			self.subscribers[trigger_name].append(callback)
		else:
			self.subscribers[trigger_name] = [callback]

	def fire_trigger(self, trigger):
		if self.subscribers.has_key(trigger.name):
			for sub in self.subscribers[trigger.name]:
				sub(trigger)
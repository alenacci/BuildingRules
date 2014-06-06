import time

class Bulletin:

	def __init__ (self):
		self.user = None
		self.state = None
		self.building = None
		self.room = None
		self.timestamp = None

	def __init__ (self, user, state, building, room):
		self.user = user
		self.state = state
		self.building= building
		self.room = room
		self.timestamp = time.time()

	def __eq__(self, obj):
		return isinstance(obj, Bulletin) \
			and obj.user == self.user \
			and obj.state == self.state \
			and obj.building == self.building \
			and obj.room == self.room

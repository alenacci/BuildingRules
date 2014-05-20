class Bulletin:

	def __init__ (self):
		self.user = None
		self.state = None
		self.room = None
		self.building = None

	def __init__ (self, user, state, building, room):
		self.user = user
		self.state = state
		self.room = room
		self.building= building

	def __eq__(self, obj):
		return isinstance(obj, Bulletin) \
			and obj.user == self.user \
			and obj.state == self.state \
			and obj.room == self.room \
			and obj.building == self.building
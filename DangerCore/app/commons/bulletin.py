
class Bulletin:

	def __init__ (self):
		self.danger_type = None
		self.room = None
		self.building = None

	def __init__ (self, danger_type, room, building):
		self.danger_type = danger_type
		self.room = room
		self.building= building

	def __eq__(self, obj):
		return isinstance(obj, Bulletin) \
			and obj.danger_type == self.danger_type \
			and obj.room == self.room \
<<<<<<< HEAD
			and obj.building == self.building
=======
			and obj.building == self.building
>>>>>>> f514ab872f1fcd9c2c62aab98c74f62c6bdea1d7

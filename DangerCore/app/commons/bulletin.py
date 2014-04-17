
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
			and obj.building == self.building

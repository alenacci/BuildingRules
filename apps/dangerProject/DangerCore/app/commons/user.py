class User:


	def __init__ (self, user_id, room, telephone=None, status=None, last_access=None):
		self.user_id = user_id
		self.room = room
		self.telephone = telephone
		self.status = status
		self.last_access = last_access

	def __eq__(self, obj):
		return isinstance(obj, User) \
			and obj.user_id == self.user_id

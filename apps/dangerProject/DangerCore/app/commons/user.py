class User:


	def __init__ (self, user_id, telephone=None, status=None, last_access=None):
		self.name = user_id
		self.telephone = telephone
		self.status = status
		self.last_access = last_access

	def __eq__(self, obj):
		return isinstance(obj, User) \
			and obj.user_id == self.user_id

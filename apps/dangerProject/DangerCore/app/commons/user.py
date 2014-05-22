class User:


	def __init__ (self, name, telephone=None, status=None, last_access=None):
		self.name = name
		self.telephone = telephone
		self.status = status
		self.last_access = last_access

	def __eq__(self, obj):
		return isinstance(obj, User) \
			and obj.name == self.name

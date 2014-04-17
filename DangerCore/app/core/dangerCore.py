from app.commons.bulletin import Bulletin

class DangerCore:

	def __init__(self):
		self.bulletin_list = []

	def handle_new_bulletin(self, bulletin):
		if self.is_active(bulletin) == False:
			self.bulletin_list.append(bulletin)
			print("new bulletin received")
		else:
			print("Ignored")

	def is_active(self, bulletin):
<<<<<<< HEAD
		if bulletin.danger_type == "GENERIC_DANGER":
			for b in self.bulletin_list:
				if b.building == bulletin.building:
					return True
			return False
		else:
			for b in self.bulletin_list:
				if b.__eq__(bulletin):
					return True
			return False
=======
		for b in self.bulletin_list:
			if b.__eq__(bulletin):
				return True
		return False
>>>>>>> f514ab872f1fcd9c2c62aab98c74f62c6bdea1d7

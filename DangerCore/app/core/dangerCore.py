from app.commons.bulletin import Bulletin

class DangerCore:

	def __init__(self):
		self.bulletin_list = []

	def handle_new_bulletin(self, bulletin):
		#TODO check for equality
		self.bulletin_list.append(bulletin)
		print("new bulletin received")
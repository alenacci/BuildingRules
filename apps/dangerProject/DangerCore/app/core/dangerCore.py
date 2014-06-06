from app.commons.bulletin import Bulletin
from connectionAnalyzerRunner import ConnectionAnalyzerRunner
from connectionAnalyzer import ConnectionAnalyzer
from audioRecordsManager import AudioRecordsManager
from notificationsManager import NotificationsManager

class DangerCore:


	def __init__(self):
		self.bulletin_list = []
		self.user_list = []
		self.TEST_confirmed_from_building_manager = False
		self.audioRecordsManager = AudioRecordsManager()
		self.notificationsManager = NotificationsManager()

	def startConnectionAnalyzer(self):
		self.connection_analyzer = ConnectionAnalyzer()
		connection_analyzer_runner = ConnectionAnalyzerRunner()

	def handle_new_bulletin(self, bulletin):
		if self.is_active(bulletin) == False:
			self.bulletin_list.append(bulletin)
			print("new bulletin received")
		else:
			print("Ignored")

	def is_active(self, bulletin):
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


	def register_user(self, user):
		for u in self.user_list:
			if u.__eq__(user):
				if u.room != user.room:
					u.room = user.room
				return
		self.user_list.append(user)

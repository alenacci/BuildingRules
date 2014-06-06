##Represent a notification to the user
##the type of notification available are
#type = "danger", "action-record_audio", "empty"
class Notification:

	def __init__(self,type):
		self.type = type
		self.timestamp = 0


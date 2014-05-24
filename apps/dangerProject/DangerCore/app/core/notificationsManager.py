class NotificationsManager:



	def __init__(self):
		self.timeCount = 1
		self.notifications = []


	def getNotificationsFromTime(self, time):
		for i,n in enumerate(self.notifications):
			if n.timestamp > time:
				return self.notifications[i:]
		return []

	def addNotification(self,n):
		self.timeCount += 1
		n.timestamp = self.timeCount
		self.notifications.append(n)

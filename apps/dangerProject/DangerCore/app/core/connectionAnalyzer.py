from app.commons.user import User
import time

class ConnectionAnalyzer:

	POLLING_TIME = 1
	DESIRED_ACCURACY = 0.97
	DOWN_TIME = 2*POLLING_TIME

	def __init__(self):
		self.user_list = []

	# This method set all users status to disconnected if they all haven't made a request for more than POLLING_TIME
	def analyze_user_list(self):
		if len(self.user.user_list) > 0 and \
				self.accuracy(time.time() - self.user_list[0].last_access) > self.DESIRED_ACCURACY:
			self.set_all_disconnected()
		else:
			for u in self.user_list:
				if u.last_access > self.DOWN_TIME:
					u.status = "disconnected"


	def set_all_disconnected(self):
		for u in self.user_list:
			u.status = "disconnected"

	def update_user_in_list(self, user_id):
		if User(user_id) in self.user_list:
			i = self.user_list.index(User(user_id))
			user = self.user_list.pop(i)
			user.last_access = time.time()
			self.user_list.insert(0, user)

	def accuracy(self, t):
		return pow((self.POLLING_TIME - t)/self.POLLING_TIME,len(self.user_list))


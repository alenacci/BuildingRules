from app.commons.user import User
from threading import Lock
import time

class ConnectionAnalyzer:

	POLLING_TIME = 30
	DESIRED_ACCURACY = 0.97
	DOWN_TIME = 2*POLLING_TIME

    def __init__(self):
		self.user_list = []
		self.lock = Lock()

		self.user_list.append(User("Andre", "3478337411", "connected", time.time()))
		self.user_list.append(User("Giada", "3401225920", "connected", time.time()))
		self.user_list.append(User("Padu", "4753675862", "connected", time.time()))
		self.user_list.append(User("Daniele", "3746287364", "connected", time.time()))
		self.user_list.append(User("Giada", "344353455", "connected", time.time()))
		self.user_list.append(User("Nacci", "4753675862", "connected", time.time()))
		self.user_list.append(User("Simone", "3746287364", "connected", time.time()))
		self.user_list.append(User("Enrico", "343776650", "connected", time.time()))
		self.user_list.append(User("Chicco", "4753675862", "connected", time.time()))
		self.user_list.append(User("Riccardo", "3746287364", "connected", time.time()))
		self.user_list.append(User("Federico", "3401923123", "connected", time.time()))
		self.user_list.append(User("Sara", "4753675862", "connected", time.time()))
		self.user_list.append(User("Anna", "3746287364", "connected", time.time()))
		self.user_list.append(User("Rita", "342293910", "connected", time.time()))
		self.user_list.append(User("Fabiola", "4753675862", "connected", time.time()))
		self.user_list.append(User("Serena", "3746287364", "connected", time.time()))



	# This method set all users status to disconnected if they all
	# haven't made a request for more than POLLING_TIME.
	# Otherwise if an user does not respond for more than DOWN_TIME,
	# he is set into disconnected status.
	def analyze_user_list(self):
		if len(self.user_list) > 0 and \
				self.accuracy(time.time() - self.user_list[0].last_access) > self.DESIRED_ACCURACY:
			self.set_all_disconnected()

		else:
			for u in self.user_list:
				if time.time() - u.last_access > self.DOWN_TIME:
					u.status = "disconnected"
		for u in self.user_list:
			print u.user_id + " " + u.status + " " + str(u.last_access)
		print("__________________________________")


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
		if(t < self.POLLING_TIME):
			print "ACCURACY = " + str(1 - pow((float(self.POLLING_TIME - t)/self.POLLING_TIME),len(self.user_list)))
			return 1 - pow((float(self.POLLING_TIME - t)/self.POLLING_TIME),len(self.user_list))
		return 1


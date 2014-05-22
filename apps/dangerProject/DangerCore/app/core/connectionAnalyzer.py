from app.commons.user import User
import time

class ConnectionAnalyzer:

    POLLING_TIME = 1

    def __init__(self):
		self.user_list = []

    # This method set all users status to disconnected if they all haven't made a request for more than POLLING_TIME
    def analyze_user_list(self):
        if len(self.user.user_list) > 0 and \
                        self.user_list[0].last_access < time.time() - ConnectionAnalyzer.POLLING_TIME:
            self.set_all_disconnected()


    def set_all_disconnected(self):
        for u in self.user_list:
            u.status = "disconnected"

    def update_user_in_list(self, name):
        if User(name) in self.user_list:
            i = self.user_list.index(User(name))
            user = self.user_list.pop(i)
            user.last_access = time.time()
            self.user_list.insert(0, user)


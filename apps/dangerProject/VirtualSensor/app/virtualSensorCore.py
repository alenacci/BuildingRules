import json, urllib2,threading
from app import app
from app.bulletin import Bulletin


#Request Rules to update the real time rules
def request_rules_real_time_update_async():
		threading.Thread(target=request_rules_real_time_update).start()

#Request Rules to update the real time rules
def request_rules_real_time_update():
		urllib2.urlopen("http://localhost:5003/api/realtime/request_update").read()

class VirtualSensorCore:

	THRESHOLD = 1

	def __init__(self):
		self.bulletin_list = []
		self.trigger_run = None

	def handle_new_bulletin(self, bulletin):
		if bulletin.state=="running":
			if self.is_active(bulletin) == False:
				self.bulletin_list.append(bulletin)
				print("new bulletin received")
				self.checkTreshold()
			else:
				print("Ignored")
		elif bulletin.state == "quiet":
			opposite = Bulletin(bulletin.user, "running", bulletin.building, bulletin.room)
			if self.is_active(opposite):
				self.bulletin_list.remove(opposite)
				print("bulletin removed")
			else:
				print("Ignored")

	def is_active(self, bulletin):
			for b in self.bulletin_list:
				if b.__eq__(bulletin):
					return True
			return False

	def checkTreshold(self):

		over_threshold = False

		#TODO rendere efficiente evitando scansioni ripetute
		for b in self.bulletin_list:
			count = 1
			for b2 in self.bulletin_list:
				if b.room == b2.room and b.building == b2.building and b.user != b2.user:
					count += 1

			if count >= self.THRESHOLD:
#				data = {
#				'danger_type' : "escape",
#				'buildings': b.buildings,
#				'room' : b.room
#				}

#				req = urllib2.Request('http://localhost:2001/api/send_bulletin')
#				req.add_header('Content-Type', 'application/json')

#				response = urllib2.urlopen(req, json.dumps(data))
				over_threshold = True
				self.trigger_run = {'room':b.room, 'building':b.building}


		if over_threshold:
			request_rules_real_time_update_async()


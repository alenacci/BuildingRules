import json, urllib2,threading
from app import app
from app.bulletin import Bulletin
import time

IP = "192.168.43.172"

#Request Rules to update the real time rules
def request_rules_real_time_update_async():
		threading.Thread(target=request_rules_real_time_update).start()

#Request Rules to update the real time rules
def request_rules_real_time_update():
		urllib2.urlopen("http://"+ IP +":5003/api/realtime/request_update").read()

class VirtualSensorCore:

	UPDATE_PERIOD = 5
	MIN_OCCUPIERS = 4

	def __init__(self):
		self.bulletin_list = []
		self.trigger_run = None
		# Start update bulletin_list thread
		t = threading.Timer(self.UPDATE_PERIOD, self.update_bulletin_list)
		t.daemon = True
		t.start()
		self.lock = threading.Lock()

	# Manage the arrival of a new bulletin.
	# If it is already present in the list its timestamp is updated
	def handle_new_bulletin(self, bulletin):
		if bulletin.state=="running":
			self.lock.acquire()
			if self.is_active(bulletin) == False:
				self.bulletin_list.append(bulletin)
				print("new bulletin received")
			else:
				for b in self.bulletin_list:
					if b.__eq__(bulletin):
						b.timestamp = bulletin.timestamp
				print("Updated")
			self.lock.release()
			self.checkTreshold()

	def is_active(self, bulletin):
			for b in self.bulletin_list:
				if b.__eq__(bulletin):
					return True
			return False

	def checkTreshold(self):

		over_threshold = False
		rooms = self.get_room_list()



		for room in rooms :
			occupiers = self.users_in_room(room)
			THRESHOLD = occupiers/2 + 1
			runners = self.run_occurrences(room)

			print "RUNNING" + str(runners) + "/" + str(occupiers) + " Room " + str(room)

			if occupiers > VirtualSensorCore.MIN_OCCUPIERS and runners > THRESHOLD:
				print "ALARM!!"

#				data = {
#				'danger_type' : "escape",
#				'buildings': b.buildings,
#				'room' : b.room
#				}

#				req = urllib2.Request('http://localhost:2001/api/send_bulletin')
#				req.add_header('Content-Type', 'application/json')

#				response = urllib2.urlopen(req, json.dumps(data))
				over_threshold = True
				# TODO manage building
				self.trigger_run = {'room':room, 'building':"BUILDING"}


		if over_threshold:
			request_rules_real_time_update_async()

	def get_room_list(self):
		rooms = []
		for b in self.bulletin_list:
			if b.room not in rooms:
				rooms.append(b.room)
		return rooms

	def run_occurrences(self,room):
		count = 0
		for b in self.bulletin_list:
			if b.room == room and b.state == "running":
				count += 1
		return count

	# Determine the number of users inside a room making a REST request to DangerCore (in future: BuildingDepot)
	def users_in_room(self, room):

		message = {
			'room'	: room
		}

		req = urllib2.Request('http://' + IP + ':2001/api/get_users')
		req.add_header('Content-Type', 'application/json')

		try:
			response = json.loads(urllib2.urlopen(req, json.dumps(message)).read())
			count = int(response['users'])
		except Exception, e:
			print str(e) + " unable to connect to dangerCore (depot)"
		return count

	# Removes all bulletin that are older than 5 seconds
	def update_bulletin_list(self):
		print "PIRMA"
		self.lock.acquire()
		remove_list = []
		for bulletin in self.bulletin_list:
			if time.time() - bulletin.timestamp > self.UPDATE_PERIOD:
				remove_list.append(bulletin)
		print "AAA" + str(len(remove_list))

		for bulletin in remove_list:
			self.bulletin_list.remove(bulletin)
		self.lock.release()

		t = threading.Timer(self.UPDATE_PERIOD, self.update_bulletin_list)
		t.daemon = True
		t.start()



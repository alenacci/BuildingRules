import buildings.building
import agents
from commons.point import *
import behaviors.behavior as behavior
import random
import concurrent.futures
import utils
import dangers

#simulator
sim = None

def init():
	global sim
	sim = Simulator()
	return sim

class Simulator:

	def __init__(self):
		self.start_time = utils.worldTime()
		self.building = None
		#to be used for background, async computations
		self.background_executor = concurrent.futures.ProcessPoolExecutor()
		pass


	def setup(self):
		self.setupBuilding()
		self.setupEnvironment()

	def setupBuilding(self):
		self.building = buildings.building.Building()
		self.building.load_rooms()
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		print str(self.building.random_room())
		self.building.create_toilets()

	def setupEnvironment(self):
		##fill up the environment with agents

		self.agents = []

		for i in range(0,50):
			agent = agents.Agent()

			#random position
			pos = self.building.random_room().random_position()
			agent.setPosition(pos)

			self.agents.append(agent)
			beh = behavior.Behavior()
			agent.behavior = beh

			beh.start()


	def update(self):
		for a in self.agents:
			#if utils.worldTime() - self.start_time > 10 or self.building.room_at_position(a.p) == "Room 3":
			#	print self.building.room_at_position(a.p) == "Room 3"
			#	a.alert = dangers.FireDanger(3)
			a.update()
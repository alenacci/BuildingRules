import buildings.building
import agents
from commons.point import *
import behaviors.behavior as behavior
import random


#simulator
sim = None

def init():
	global sim
	sim = Simulator()
	return sim

class Simulator:

	def __init__(self):
		self.building = None
		pass


	def setup(self):
		self.setupBuilding()
		self.setupEnvironment()

	def setupBuilding(self):
		self.building = buildings.building.Building()
		self.building.load_rooms()

	def setupEnvironment(self):
		##fill up the environment with agents

		self.agents = []


		for i in range(0,5):
			agent = agents.Agent()

			#random position
			w = self.building.grid.GRID_WIDTH
			h = self.building.grid.GRID_HEIGHT
			randw = random.randint(0,w-1)
			randh = random.randint(0,h-1)
			agent.setPosition(Point(randw,randh))

			self.agents.append(agent)
			beh = behavior.Behavior()
			agent.behavior = beh

			beh.start()

	def update(self):
		for a in self.agents:
			a.update()
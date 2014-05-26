from building.grid import Grid
from agents import *
from behaviors.actions.moveAction import *
from commons.point import *
from behaviors.behavior import *
import random


#simulator
sim = None

def init():
	global sim
	sim = Simulator()
	return sim

class Simulator:

	def __init__(self):
		self.grid = Grid("./res/map_grid.png")



	def setupEnvironment(self):
		##fill up the environment with agents

		self.agents = []


		for i in range(0,5):
			agent = Agent()

			#random position
			w = simulator.sim.grid.GRID_WIDTH
			h = simulator.sim.grid.GRID_HEIGHT
			randw = random.randint(0,w-1)
			randh = random.randint(0,h-1)
			agent.setPosition(Point(randw,randh))

			self.agents.append(agent)
			beh = Behavior()
			agent.behavior = beh

			beh.newAction()

	def update(self):
		for a in self.agents:
			a.update()
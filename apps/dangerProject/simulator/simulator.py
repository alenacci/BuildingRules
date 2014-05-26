from building.grid import Grid
from agents import *
from behaviors.actions.moveAction import *
from commons.point import *
from behaviors.behavior import *

#simulator
sim = None

def init():
	global sim
	sim = Simulator()
	return sim

class Simulator:

	def __init__(self):
		self.grid = Grid("./res/map_grid2.png")



	def setupEnvironment(self):
		self.agents = []
		age1 = Agent()
		self.agents.append(age1)

		beh = Behavior()
		age1.behavior = beh

		beh.newAction()

	def update(self):
		for a in self.agents:
			a.update()
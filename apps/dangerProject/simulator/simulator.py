from building.grid import Grid
from agents import *
from behavior.actions.moveAction import *
from commons.point import *

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
		self.agents = []
		age1 = Agent()
		self.agents.append(age1)

		action = MoveAction(age1,Point(3,3),Point(45,5))
		age1.setCurrentAction(action)

		action.start()

	def update(self):
		for a in self.agents:
			a.update()
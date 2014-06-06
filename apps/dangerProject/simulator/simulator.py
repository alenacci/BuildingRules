import buildings.building
import agents
from commons.point import *
import behaviors.behavior as behavior
import random
import concurrent.futures

import dangers
from triggers.trigger_manager import TriggerManager
import modules
from utils.worldTime import worldTime
from triggers.trigger import Trigger
from behaviors.escape_behavior import EscapeBehavior


#simulator
sim = None

def init():
	global sim
	sim = Simulator()
	return sim

class Simulator:

	MAX_BACKGROUND_THREAD_WORKERS = 4

	def __init__(self):
		self.building = None
		#to be used for background, async computations
		self.background_executor = concurrent.futures.ThreadPoolExecutor(Simulator.MAX_BACKGROUND_THREAD_WORKERS)
		self.modules = []
		self.trigger_manager = TriggerManager()
		self.time = None
		pass

	def load_modules(self):
		"""load and init all the modules present in the modules package"""
		modules.load_modules()
		for cls in modules.modules_classes:
			self.modules.append(cls(self))
			print("Load module: " + str(cls))

	def after_populate(self):
		"""call the method of the modules after the building is populated"""
		for m in self.modules:
			m.after_populate(self.agents)

	def setup(self, load_modules=True):
		if load_modules:
			self.load_modules()
		self.setupBuilding()
		self.setupEnvironment()
		self.after_populate()

		self.start_time = worldTime()
		self.time = 0

	def setupBuilding(self):
		self.building = buildings.building.Building()
		self.building.load_rooms()
		self.building.create_toilets()

	def setupEnvironment(self):
		##fill up the environment with agents

		self.agents = []

		for i in range(0, 80):
			agent = agents.Agent()

			#random position
			pos = self.building.random_room().random_position()
			agent.setPosition(pos)

			self.agents.append(agent)
			beh = behavior.Behavior()
			agent.behavior = beh

			beh.start()



	def update(self):
		self.time = worldTime() - self.start_time



		for a in self.agents:
			a.update()
			#update modules
			for mod in self.modules:
				try:
					mod.update_agent(a, self.time)
				except Exception:
					mod.handle_exception()

		#update modules
		for mod in self.modules:
			try:
				mod.update(self.time)
			except Exception:
				mod.handle_exception()


		#if self.time%3 > 0 and self.time%3 < .1:
		'''if self.time > 3 and self.time < 3.10:
			room = self.building.random_room()
			self.trigger_manager.fire_trigger(Trigger("fire", room, room.random_position()))'''

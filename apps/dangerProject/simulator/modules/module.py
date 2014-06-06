import traceback
import sys

class Module(object):
	"""Base class for all the modules"""

	def __init__(self, simulator):
		self.simulator = simulator

	def handle_exception(self):
		print "Error in module " + self.__class__.__name__
		traceback.print_exc(file=sys.stdout)

	""" init method """
	def after_populate(self, agents):
		"""called after the agents are put into the map"""
		pass


	""" update methods """
	def update(self, time):
		"""called every simulation cycle"""
		pass

	def update_agent(self, agent, time):
		"""called for each agent after being updated"""
		pass

	""" render methods """

	def render_background(self, window):
		pass

	def render_building(self, window):
		pass

	def render_agent(self, window, agent):
		pass

	def render_foreground(self, window):
		pass


import traceback
import sys

class Module(object):
	"""Base class for all the modules"""

	def __init__(self, simulator):
		self.simulator = simulator

	def handle_exception(self):
		print "Error in module " + self.__class__.__name__
		traceback.print_exc(file=sys.stdout)


	def after_populate(self, agents):
		pass

	def render_background(self, window):
		pass

	def render_building(self, window):
		pass

	def render_agent(self, window, agent):
		pass

	def update(self, time):
		pass

	def update_agent(self, agent, time):
		pass
import tasks.toiletTask
import commons
import random
import simulator
import utils
from behavior import Behavior
from tasks.escapeTask import EscapeTask
from actions.moveAction import MoveAction
from commons.point import Point


''' behaviors for people escaping from the building'''
class EscapeBehavior(Behavior):

	def __init__(self):
		self.agent = None
		self.task = None
		#list of rects where people should escape
		self.escape_regions = []

	def start(self):
		self.task = EscapeTask(self.agent, random.choice(self.escape_regions))
		self.task.end.connect(self.onEscapeEnded, False)
		self.task.start()

		#ESCAPE BEHAVIOR IS TRASMISSIBLE
		self.agent.on_meet_others.connect(self._on_meet_others, False)


	def onEscapeEnded(self):
		print "safe!"

	def stop(self):
		if self.task is not None:
			self.task.stop()

	def update(self):
		"""Now is quite useless"""
		pass

	def _on_meet_others(self,others):
		for a in others:
			if a.behavior.__class__.__name__ != "EscapeBehavior":
				print "INFECTED"
				a.behavior.stop()
				a.behavior = EscapeBehavior()
				a.behavior.escape_regions = self.escape_regions
				a.behavior.start()


from behavior import Behavior
import tasks.fireTask
import tasks.escapeTask


class FireBehavior(Behavior):

	def __init__(self):
		self.agent = None
		self.task = None
		#list of rects where people should escape
		self.escape_regions = []



	def start(self, fire):
		#print " ___________"
		#print "| ALERT!!!! |"
		#print "'''''''''''''"
		self.fire_task = tasks.fireTask.FireTask(self.agent, fire)
		self.fire_task.end.connect(self.escape, False)
		#print str(self.task)
		self.fire_task.start()

	def escape(self):
		self.escape_task = tasks.escapeTask.EscapeTask(self.agent, self.escape_regions[0])
		self.escape_task.start()


	def stop(self):
		if self.task is not None:
			self.task.stop()
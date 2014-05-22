import sched, time, threading
from app import app


class ConnectionAnalyzerRunner:

	s = sched.scheduler(time.time, time.sleep)

	def __init__(self):
		print "start"
		self.count = 0
		self.periodic_analysis()


	def periodic_analysis(self):
		connectionAnalyzer = app.danger_core.connection_analyzer
		connectionAnalyzer.lock.acquire()
		connectionAnalyzer.analyze_user_list()
		connectionAnalyzer.lock.release()
		self.count += 1
		print "count = " + str(self.count)
		threading.Timer(1, self.periodic_analysis).start()
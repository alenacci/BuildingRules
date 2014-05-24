import sched, time, threading
from app import app


class ConnectionAnalyzerRunner:

	s = sched.scheduler(time.time, time.sleep)

	def __init__(self):
		self.periodic_analysis()


	def periodic_analysis(self):
		connectionAnalyzer = app.danger_core.connection_analyzer
		connectionAnalyzer.lock.acquire()
		connectionAnalyzer.analyze_user_list()
		connectionAnalyzer.lock.release()
		threading.Timer(1, self.periodic_analysis).start()
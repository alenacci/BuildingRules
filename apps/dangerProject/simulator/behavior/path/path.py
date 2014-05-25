from _testcapi import raise_exception
import helpers

class Path:

	def __init__(self, tiles):
		if len(tiles) == 0:
			raise Exception("Empty tiles array")


		first = self.points[0]
		prev = Path.Point(first.x,first.y)
		prev.g = 0
		self.points = [prev]

		for t in tiles:
			p = Path.Point(t.x, t.y)
			#set distance
			p.g = prev.g + p.dist(prev)
			self.points.append(p)

		self.length = self.points[-1].g

	#return the position corresponding to the
	#given percentage along the path
	def getPositionAtPercentage(self, percentage):

		if percentage > 1:
			percentage = 1
		elif percentage < 0:
			percentage = 0

		dist = percentage * self.length

		for i, p in enumerate(self.points):
			if p.g < dist and

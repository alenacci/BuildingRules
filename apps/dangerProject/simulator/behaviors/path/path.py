from commons.point import Point

class Path(object):

	def __init__(self, tiles):
		if len(tiles) == 0:
			raise Exception("Empty tiles array")

		prev = Point(tiles[0].x, tiles[0].y)
		prev.g = 0
		self.points = [prev]

		for t in tiles[1:]:
			p = Point(t.x, t.y)
			#set distance
			p.g = prev.g + p.dist(prev)
			self.points.append(p)
			prev = p

		self.start = self.points[0]
		self.end = self.points[-1]
		self.length = self.end.g

	@property
	def start(self):
		return self.points[0]

	@start.setter
	def start(self, p):
		self.points[0] = p

	@property
	def end(self):
		return self.points[-1]

	@end.setter
	def end(self, p):
		self.points[-1] = p

	#return the position corresponding to the
	#given percentage along the path
	def getPositionAtPercentage(self, percentage):

		if percentage >= 1:
			return self.end
		elif percentage <= 0:
			return self.start

		#if the path is one node only
		if len(self.points) == 1:
			return self.start

		dist = percentage * self.length
		previousPoint = self.start
		nextPoint = self.points[1]

		for i in range(1,len(self.points)-1):
			p = self.points[i]
			next = self.points[i+1]

			if p.g < dist and next.g > dist:
				previousPoint = p
				nextPoint = next
				break

		remaining = dist - previousPoint.g
		delta = (nextPoint - previousPoint).normalize() * remaining
		return (previousPoint + delta)

	def __str__(self):
		ret = "path of length=" + str(self.length) + " and points=" + str(len(self.points))
		for p in self.points:
			ret += "\n " + str(p) + " at distance: " + str(p.g)
		return ret

	#has to be called after every change in the position
	#of the nodes
	def recomputeDistances(self):
		prev = self.points[0]
		prev.g = 0

		for point in self.points[1:]:
			#set distance
			point.g = prev.g + point.dist(prev)
			prev = point

		self.start = self.points[0]
		self.end = self.points[-1]
		self.length = self.end.g

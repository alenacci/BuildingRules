from commons.point import Point

class Path:

	def __init__(self, tiles):
		if len(tiles) == 0:
			raise Exception("Empty tiles array")

		prev = Point(tiles[0].x,tiles[0].y)
		prev.g = 0
		self.points = [prev]

		for t in tiles:
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

	@start.setter
	def end(self, p):
		self.points[-1] = p

	#return the position corresponding to the
	#given percentage along the path
	def getPositionAtPercentage(self, percentage):

		if percentage >= 1:
			return self.end
		elif percentage <= 0:
			return self.start

		dist = percentage * self.length
		previousPoint = None
		nextPoint = None


		for i in range(1,len(self.points)-1):
			p = self.points[i]
			next = self.points[i+1]
			if p.g < dist and next.g > dist:
				previousPoint = p
				nextPoint = next
				break

		remaining = dist - previousPoint.g
		rem_perc = remaining / self.length
		delta = (nextPoint - previousPoint).normalize() * remaining
		return (previousPoint + delta)

	def __str__(self):
		return "path of length=" + str(self.length) + " and points=" + str(len(self.points))
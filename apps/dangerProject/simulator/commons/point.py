import math

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		#distance from start
		#used in path
		self.g = 0

	def tr(self, x, y):
		self.x += x
		self.y += y
		return self

	def rot(self, rad=0):
		x = self.x * math.cos(rad) - self.y * math.sin(rad)
		y = self.x * math.sin(rad) + self.y * math.cos(rad)
		self.x = x
		self.y = y
		return self

	def dup(self):
		return Point(self.x, self.y)

	def dot(self, v):
		return self.x * v.x + self.y * v.y

	def __eq__ (self, v):
		if not type(v) == Point:
			return False
		if self.x == v.x and self.y == v.y:
			return True
		return False

	def __add__ (self, v):
		return self.dup().tr(v.x, v.y)

	def __sub__ (self, v):
		return self.dup().tr(-v.x, -v.y)

	def __mul__ (self, m):
		return Point(self.x * m, self.y * m)

	def __neg__ (self):
		return self * (-1)

	def __str__ (self):
		return "(%.2f, %.2f)" % (self.x, self.y)

	def to_a (self):
		return [self.x, self.y]

	@property
	def length(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	@length.setter
	def length(self, l):
		self.normalize()
		self.x *= l
		self.y *= l

	def normalize(self):
		l = self.length
		self.x /= l
		self.y /= l
		return self

	def perpendicular(self):
		return Point(-self.y, self.x)

	def dist(self,p):
		return self.distance(self.x,self.y,p.x,p.y)

	def distance(self, sx,sy,ex,ey):
		return math.sqrt( (ex-sx)**2 + (ey-sy)**2 )


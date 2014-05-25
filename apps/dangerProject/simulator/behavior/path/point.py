import helpers

class Point:
		def __init__(self,x,y):
			self.x = x
			self.y = y
			#distance from start
			self.g = 0

		def dist(self,p):
			return helpers.distance(self.x,self.y,p.x,p.y)
import helpers

##Execute some functions to the "raw" path
#generated from astar in order to make it more
#"smooth"

class Postprocessor:
	#the path is just an array of tiles
	def __init__(self, tiles, path):
		if len(path) == 0:
			raise Exception("Empty path")
		self.path = path
		self.tiles = tiles

	def simplify(self):
		pivots = [self.path[0]]
		last_corner = self.path[0]

		#skip the last item
		for i, t in enumerate(self.path):
			if not helpers.checkStraightPath(self.tiles, \
				last_corner.x, last_corner.y, t.x, t.y):
				previous = self.path[i-1]
				pivots.append(previous)
				last_corner = previous

		#add the last
		pivots.append(self.path[-1])

		return pivots



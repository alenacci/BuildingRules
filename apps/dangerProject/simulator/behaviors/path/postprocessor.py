import helpers

##Execute some functions to the "raw" path
#generated from astar in order to make it more
#"smooth"

class Postprocessor:
	#the path is just an array of tiles
	def __init__(self, tiles, path_tiles):
		if len(path_tiles) == 0:
			raise Exception("Empty path")
		self.path = path_tiles
		self.tiles = tiles

	def simplify(self):

		pivots = [self.path[0]]
		last_corner = self.path[0]

		#skip the last item
		for i, t in enumerate(self.path[1:]):
			if not helpers.checkStraightPath(self.tiles, \
						last_corner.x, last_corner.y, t.x, t.y):

				previous = self.path[i] #is not i-1 because the enumerations starts from 1:
				pivots.append(previous)
				last_corner = previous

		#add the last
		pivots.append(self.path[-1])
		return pivots



#Is the most little block of
#our building.
class Tile:

	def __init__(self, x, y, room = None, walkable = True):
		#x and y are the position
		#in the grid
		self.x = x
		self.y = y
		self.walkable = True
		self.room = room


	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __str__(self):
		w = " - walkable" if self.walkable else " - not walkwable"
		return "tile (" + str(self.x) + ", " + str(self.y) + ") " + w

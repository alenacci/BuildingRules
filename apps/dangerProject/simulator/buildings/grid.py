import scipy.misc
from tile import Tile

#Represent an array of tiles
class Grid:

	# initialize an empty grid
	def __init__(self, width, height):
		self.GRID_WIDTH = width
		self.GRID_HEIGHT = height
		self.tiles = [[Tile(y,x) for x in xrange(self.GRID_WIDTH)] for y in xrange(self.GRID_HEIGHT)]


	def __init__(self, image_path):
		img = scipy.misc.imread(image_path,True)
		self.GRID_WIDTH = len(img[0])
		self.GRID_HEIGHT = len(img)

		self.tiles = [[Tile(y,x) for x in xrange(self.GRID_WIDTH)] for y in xrange(self.GRID_HEIGHT)]

		for i in range(0,self.GRID_WIDTH):
			for j in range(0, self.GRID_HEIGHT):
				self.tiles[j][i].walkable = (img[i][j] == 255.0)

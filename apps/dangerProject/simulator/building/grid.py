import scipy.misc

#Represent an array of tiles
class Grid:

	# initialize an empy grid
	def __init__(self, width, height):
		self.GRID_WIDTH = width
		self.GRID_HEIGHT = height
		self.tiles = [[Tile(x,y) for x in xrange(Grid.GRID_WIDTH)] for y in xrange(Grid.GRID_HEIGHT)]


	def __init__(self, image_path):
		img = scipy.misc.imread(image_path,True)
		self.GRID_WIDTH = len(img[0])
		self.GRID_HEIGHT = len(img)

		self.tiles = [[Tile(x,y) for x in xrange(Grid.GRID_WIDTH)] for y in xrange(Grid.GRID_HEIGHT)]

		for i in range(0,self.GRID_WIDTH):
			for j in range(0, self.GRID_HEIGHT):
				self.tiles[i,j].walkable = (img[i][j] == 255.0)

	
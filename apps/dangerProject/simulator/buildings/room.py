import random
from commons.point import Point

class Room:

	def __init__(self, id, weight=1.0):
		"""weight: a value computed together with the size of the
		room to choose how probable is this room
		in being selected. For instance, a corridor should
		have a low weight"""

		self.id = id
		self.tiles = []
		###TODO spostarli
		if id == 0 or id == 15 or id==10:
			weight = 0.1

		###TODO bagno
		if id == 8:
			weight = 0

		#list of agents in this room
		self.agents = []

		self.weight = weight

	def __str__(self):
		return "Room " + str(self.id)

	def __eq__(self, other):
		return type(other) is Room and other.id == self.id

	#return the size of the room as number of tiles
	@property
	def size(self):
		return len(self.tiles)

	def random_tile(self):
		return random.choice(self.tiles)

	def random_position(self):
		tile = self.random_tile()
		return Point(tile.x, tile.y)

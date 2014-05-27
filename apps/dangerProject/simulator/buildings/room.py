import random
from commons.point import Point

class Room:

	def __init__(self, id):
		self.id = id
		self.tiles = []

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

from buildings import *
import random

class Building:

	def __init__(self):
		self.grid = Grid("./res/map_grid2.png")
		self.rooms = []
		self.size = 0

	def load_rooms(self):
		self.room_generator = RoomGenerator("./res/map_rooms2.png")
		self.update_size()

	#pick a random room with a probability weighted on the size of the room
	def random_room(self):
		rand = random.randint(0, self.size)
		_sum = 0

		for r in self.rooms:
			_sum += r.size
			if _sum >= rand:
				return r

	#update size of the building as sum of the sizes of the rooms
	def update_size(self):
		self.size = 0
		for r in self.rooms:
			self.size += r.size

	def room_at_position(self, p):

		if p.x >= self.grid.GRID_WIDTH or p.y >= self.grid.GRID_HEIGHT:
			return None

		tile = self.grid.tiles[int(p.x)][int(p.y)]

		if tile.room != None:
			return self.rooms[tile.room]
		else:
			return None



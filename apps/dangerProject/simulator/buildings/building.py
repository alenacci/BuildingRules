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

	def random_room(self):
		"""pick a random room with a probability weighted on the size of the room
		and the weight of the room"""


		tot_weight = 0.0

		for r in self.rooms:
			tot_weight += int(r.weight * r.size)

		rand = random.randint(0, tot_weight)
		_sum = 0

		for r in self.rooms:
			_sum += r.size * r.weight
			if _sum >= rand:
				return r

	def update_size(self):
		"""update size of the building as sum of the sizes of the rooms"""

		self.size = 0
		for r in self.rooms:
			self.size += r.size

	def room_at_position(self, p):

		if p.x >= self.grid.GRID_WIDTH or p.y >= self.grid.GRID_HEIGHT:
			return None

		tile = self.grid.tiles[int(p.x)][int(p.y)]

		if tile.room is not None:
			return self.rooms[tile.room]
		else:
			return None



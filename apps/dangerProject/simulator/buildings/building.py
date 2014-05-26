from buildings import *

class Building:

	def __init__(self):
		self.grid = Grid("./res/map_grid2.png")

	def load_rooms(self):
		self.room_generator = RoomGenerator("./res/map_rooms2.png")
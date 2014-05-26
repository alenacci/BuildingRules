import scipy.misc
from tile import Tile
import numpy as np
from room import Room

#import info about the rooms from
#a image
class RoomGenerator:
	colors = []

	def __init__(self, image_path):
		self.img = scipy.misc.imread(image_path)
		self.GRID_WIDTH = len(self.img[0])
		self.GRID_HEIGHT = len(self.img)
		self.WHITE = [255,255,255]
		RoomGenerator.colors = []
		for j in range (0, self.GRID_HEIGHT):
			RoomGenerator.colors.insert(j, self.img[j][self.GRID_WIDTH-1])

		import simulator
		building = simulator.sim.building
		self.tiles = building.grid.tiles


		for j in range(0, self.GRID_HEIGHT):
			if self.img[j][self.GRID_WIDTH-1][0] == self.WHITE[0] and \
				self.img[j][self.GRID_WIDTH-1][1] == self.WHITE[1] and \
				self.img[j][self.GRID_WIDTH-1][2] == self.WHITE[2]:
				break
			room = Room(j)
			building.rooms.append(room)
			self.assign_room(room)


	def assign_room(self, room):
		room_num = room.id
		for j in range(0, self.GRID_HEIGHT):
			for i in range(0, self.GRID_WIDTH - 1):
				if self.img[j][i][0] == RoomGenerator.colors[room_num][0] and \
					self.img[j][i][1] == RoomGenerator.colors[room_num][1] and \
					self.img[j][i][2] == RoomGenerator.colors[room_num][2]:
						self.tiles[i][j].room = room_num
						room.tiles.append(self.tiles[i][j])
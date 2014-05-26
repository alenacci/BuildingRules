import scipy.misc
import building
from tile import Tile
import numpy as np


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

		self.tiles = building.grid.tiles


		for j in range(0, self.GRID_HEIGHT):
			print "COL = " + str(self.img[j][self.GRID_WIDTH-1])
			if self.img[j][self.GRID_WIDTH-1][0] == self.WHITE[0] and \
				self.img[j][self.GRID_WIDTH-1][1] == self.WHITE[1] and \
				self.img[j][self.GRID_WIDTH-1][2] == self.WHITE[2]:
				break
			self.assign_room(j)


	def assign_room(self, room_num):
		for j in range(0, self.GRID_HEIGHT):
			for i in range(0, self.GRID_WIDTH - 1):
				if self.img[j][i][0] == RoomGenerator.colors[room_num][0] and \
					self.img[j][i][1] == RoomGenerator.colors[room_num][1] and \
					self.img[j][i][2] == RoomGenerator.colors[room_num][2]:
						self.tiles[i][j].room = room_num

		for row in self.tiles:
			for tile in row:
				print tile.room
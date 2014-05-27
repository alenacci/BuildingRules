import sys
import pygame
import buildings.room_generator
from commons.point import Point
import simulator

pygame.init()

class Renderer:

	WHITE = [0,0,0]
	AGENT_COLOR = [255,0,0]
	WALL_COLOR = [0,255,255]
	SIZE_X = 9
	SIZE_Y = 9
	AGENT_SIZE = 10

	def __init__(self):
		#create the screen
		self.window = pygame.display.set_mode((800, 600))
		pygame.display.set_caption('Simulator')



		#size of the map in pixels
		self.map_width_px = simulator.sim.building.grid.GRID_WIDTH * Renderer.SIZE_X
		self.map_height_px = simulator.sim.building.grid.GRID_HEIGHT * Renderer.SIZE_Y

		#high resolution image of the buildings map
		self.map_image = pygame.image.load("./res/map2.png")
		self.map_image = pygame.transform.scale(self.map_image, (self.map_width_px, self.map_height_px))

		self.agent_image = pygame.image.load("./res/agent.png")
		self.agent_image = pygame.transform.scale(self.agent_image, (self.AGENT_SIZE, self.AGENT_SIZE))

	def draw(self):
		#clear
		self.window.fill([255,255,255])

		self.drawBuilding()
		self.drawAgents()

		#draw it to the screen
		pygame.display.flip()

	def drawTile(self, tile):
		if(tile.walkable == True):
			#color = Renderer.WHITE
			if tile.room != None:
				color = buildings.room_generator.RoomGenerator.colors[tile.room]
			else:
				color = Renderer.WHITE
		else:
			color = Renderer.WALL_COLOR
		pygame.draw.rect(self.window, color, [tile.x*Renderer.SIZE_X, tile.y*Renderer.SIZE_Y,
											  Renderer.SIZE_X, Renderer.SIZE_Y])

	def drawAgents(self):

		tr = Point(self.AGENT_SIZE/2, self.AGENT_SIZE/2)

		for a in simulator.sim.agents:
			#need to translate and resize the position to center the image
			#in respect of the position
			dest_x = a.x * Renderer.SIZE_X #+ Renderer.AGENT_SIZE/2
			dest_y = a.y * Renderer.SIZE_Y #+ Renderer.AGENT_SIZE/2

			self.window.blit(self.agent_image, (dest_x, dest_y) )
			#pygame.draw.aacircle(self.window, Renderer.AGENT_COLOR, [int(a.x*Renderer.SIZE_X), int(a.y*Renderer.SIZE_Y)],\
			#				   int(Renderer.AGENT_SIZE/2))

	def drawBuilding(self):

		self.window.blit(self.map_image, (0,0))

		#Draw the grid tile by tile
		'''for row in simulator.sim.building.grid.tiles:
			for tile in row:
				self.drawTile(tile)'''



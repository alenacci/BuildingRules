import sys
#import and init pygame
import pygame
import building
pygame.init()

class Renderer:

	WHITE = [0,0,0]
	AZZURRO = [0,255,255]
	SIZE_X = 6
	SIZE_Y = 6


	def __init__(self):
		#create the screen
		self.window = pygame.display.set_mode((640, 480))
		pygame.display.set_caption('Simulator')


	def drawTile(self, tile):
		if(tile.walkable == True):
			color = Renderer.WHITE
		else:
			color = Renderer.AZZURRO
		pygame.draw.rect(self.window, color, [tile.x*Renderer.SIZE_X, tile.y*Renderer.SIZE_Y,
											  Renderer.SIZE_X, Renderer.SIZE_Y])

	def drawBuilding(self):
		for row in building.grid.tiles:
			for tile in row:
				self.drawTile(tile)


		#draw it to the screen
		pygame.display.flip()

		#input handling (somewhat boilerplate code):
		while True:
		   for event in pygame.event.get():
			  if event.type == pygame.QUIT:
				  sys.exit(0)
			  else:
				  print event


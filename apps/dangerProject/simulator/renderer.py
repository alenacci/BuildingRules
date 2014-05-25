import sys
import pygame
import building
from behavior.path import *
import time
import agents
from behavior.actions import *
from commons.point import Point
import simulator

pygame.init()

class Renderer:

	WHITE = [0,0,0]
	AGENT_COLOR = [255,0,0]
	WALL_COLOR = [0,255,255]
	SIZE_X = 6
	SIZE_Y = 6


	def __init__(self):
		#create the screen
		self.window = pygame.display.set_mode((640, 480))
		pygame.display.set_caption('Simulator')



	def draw(self):
		#clear
		self.window.fill([255,255,255])

		self.drawBuilding()
		self.drawAgents()

		#draw it to the screen
		pygame.display.flip()

	def drawTile(self, tile):
		if(tile.walkable == True):
			color = Renderer.WHITE
		else:
			color = Renderer.WALL_COLOR
		pygame.draw.rect(self.window, color, [tile.x*Renderer.SIZE_X, tile.y*Renderer.SIZE_Y,
											  Renderer.SIZE_X, Renderer.SIZE_Y])

	def drawAgents(self):
		for a in simulator.sim.agents:
			pygame.draw.rect(self.window, Renderer.AGENT_COLOR, [a.x*Renderer.SIZE_X, a.y*Renderer.SIZE_Y,
											  Renderer.SIZE_X, Renderer.SIZE_Y])

	def drawBuilding(self):
		for row in simulator.sim.grid.tiles:
			for tile in row:
				self.drawTile(tile)



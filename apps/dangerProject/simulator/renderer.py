import sys
import pygame
import buildings.room_generator
from commons.point import Point
import utils
import simulator

pygame.init()

class Renderer:

	WHITE = [0,0,0]
	#color of the noise circles
	NOISE_COLOR = [100, 100, 100]
	AGENT_COLOR = [255,0,0]
	WALL_COLOR = [0,255,255]
	SIZE_X = 9
	SIZE_Y = 9
	AGENT_SIZE = 10
	MOV_ICON_SIZE = 16

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

		self.agent_move_image = pygame.image.load("./res/mov.png")
		self.agent_move_image = pygame.transform.scale(self.agent_move_image, (self.MOV_ICON_SIZE, self.MOV_ICON_SIZE))

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

			if a.is_generating_noise:
				self.drawAgentSoundEffect(a)

			if a.is_running:
				self.drawAgentMoveEffect(a)

			#pygame.draw.aacircle(self.window, Renderer.AGENT_COLOR, [int(a.x*Renderer.SIZE_X), int(a.y*Renderer.SIZE_Y)],\
			#				   int(Renderer.AGENT_SIZE/2))



	def drawAgentSoundEffect(self, agent):
		"""Draw around the circle of the agent a series of concentric circles"""

		enhance_duration = 0.5

		start_time = agent.loud_noise_start_time
		now = utils.worldTime()
		dt = now - start_time

		def draw_circle(progress):
			max_radius = 15

			#The radius will start from the border to the agent to the max radius
			base_radius = Renderer.AGENT_SIZE/2
			radius = base_radius + (max_radius - base_radius) * progress

			pygame.draw.circle(self.window, Renderer.NOISE_COLOR, [int(agent.x*Renderer.SIZE_X + Renderer.SIZE_X/2 + 1),
																   int(agent.y*Renderer.SIZE_Y + Renderer.SIZE_Y/2 + 1)],int(radius), 1)

		progress = (dt % enhance_duration) / enhance_duration
		draw_circle(progress)

		#second circle
		if dt > enhance_duration / 2:
			progress2 = progress - 0.5 if progress > 0.5 else 1 - progress + 0.5
			draw_circle(progress2)



	def drawAgentMoveEffect(self, agent):
		"""Draw around the circle of the agent an icon for showing that it is running"""
		tr = (Renderer.MOV_ICON_SIZE - Renderer.AGENT_SIZE)/2
		dest_x = agent.x * Renderer.SIZE_X - tr
		dest_y = agent.y * Renderer.SIZE_Y - tr
		self.window.blit(self.agent_move_image, (dest_x, dest_y) )



	def drawBuilding(self):

		self.window.blit(self.map_image, (0,0))

		#Draw the grid tile by tile
		'''for row in simulator.sim.building.grid.tiles:
			for tile in row:
				self.drawTile(tile)'''



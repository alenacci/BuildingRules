from module import Module
import pygame
import renderer

class AdornmentsModule(Module):

	def __init__(self, simulator):
		Module.__init__(self, simulator)
		self.danger_image = pygame.image.load("./res/danger_icon.png")
		self.right_image = pygame.image.load("./res/right_icons.png")
		self.hpps_image = pygame.image.load("./res/hpps_icon.png")
		self.developers_image = pygame.image.load("./res/developers_icon.png")
		#self.right_image = pygame.transform.scale(self.right_image, (120, 98))
		renderer.Renderer.OFFSET_X = 135
		renderer.Renderer.OFFSET_Y = 80

	def render_background(self, window):
		window.blit(self.danger_image, (20, 10) )
		#window.blit(self.right_image, (600, 20) )
		window.blit(self.hpps_image, (21, 140) )
		window.blit(self.developers_image, (20, 80) )
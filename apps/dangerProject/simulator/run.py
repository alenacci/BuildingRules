import renderer
import utils
import building
import time
import pygame
import sys
import simulator
import random

random.seed(10)

sim = simulator.init()
r = renderer.Renderer()

sim.setupEnvironment()


while True:

	r.draw()
	sim.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		else:
			pass
			#print event




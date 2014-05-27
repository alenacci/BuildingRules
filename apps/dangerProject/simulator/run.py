import renderer

import pygame
import sys
import simulator
import random
import threading

random.seed(10)

sim = simulator.init()
sim.setup()
r = renderer.Renderer()

terminate = False

def simulate():
	while not terminate:
		sim.update()


def render():
	while True:
		r.draw()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				global terminate
				terminate = True
				sys.exit(0)
			else:
				pass
				#print event


simulation_thread = threading.Thread(target=simulate)
#render_thread = threading.Thread(target=render)

simulation_thread.start()
#render_thread.run()

render()

#render_thread.join()
#simulation_thread.join()




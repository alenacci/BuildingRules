import renderer

import pygame
import sys
import simulator
import random
import threading
import console.trigger_command

random.seed(10)

load_modules = True

if len(sys.argv) > 1 and sys.argv[1] == "no-modules":
	load_modules = False

sim = simulator.init()
sim.setup(load_modules=load_modules)
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
				simulation_thread.terminate = True

				sys.exit(0)
			else:
				pass
				#print event


simulation_thread = threading.Thread(target=simulate)
#render_thread = threading.Thread(target=render)

simulation_thread.start()
#render_thread.run()

console.trigger_command.start_console()

render()

#render_thread.join()
#simulation_thread.join()




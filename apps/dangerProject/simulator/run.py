import renderer
import utils
import building
import time

r = renderer.Renderer()
r.drawBuilding()


def computePath():
	astar = utils.astar.AStar(building.grid,3,3,45,5)

	print str(time.time())
	p = astar.computePath()
	print str(time.time())

import cProfile
cProfile.run('computePath()')
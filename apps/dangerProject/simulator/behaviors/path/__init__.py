from astar import AStar
from postprocessor import Postprocessor
from path import Path
import time

#returns none if no path is found
#otherwise returns a Path object
def findPath(grid, sx, sy, ex, ey):

	t = time.time()
	ret_value = None

	astar =  AStar(grid, sx, sy, ex, ey)
	p = astar.computePath()
	if p:
		post = Postprocessor(grid.tiles, p)
		p = post.simplify()
		ret_value = Path(p)
	else:
		ret_value = None

	dt = time.time() - t
	print "a-start: " + str(dt) + " secs"

	return ret_value
from astar import AStar
from postprocessor import Postprocessor
from path import Path

#returns none if no path is found
#otherwise returns a Path object
def findPath(grid, sx, sy, ex, ey):
	astar =  AStar(grid, sx, sy, ex, ey)
	p = astar.computePath()
	if p:
		post = Postprocessor(grid.tiles, p)
		p = post.simplify()
		return Path(p)
	else:
		return None


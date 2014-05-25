from astar import AStar
from postprocessor import Postprocessor
from path import Path

def findPath(grid, sx, sy, ex, ey):
	astar =  AStar(grid, sx, sy, ex, ey)
	p = astar.computePath()
	post = Postprocessor(grid.tiles, p)
	p = post.simplify()
	return Path(p)



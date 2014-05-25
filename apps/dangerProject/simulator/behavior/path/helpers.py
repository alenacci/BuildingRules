#return whether is possible to go from a point
#to another via a straight line
##TODO this is a really shitty implemenatation
def checkStraightPath(tiles, sx,sy,ex,ey):

	dx = 1 if sx <= ex else -1
	dy = 1 if sy <= ey else -1

	for i in range(sx,ex+dx,dx):
		for j in range(sy, ey+dy,dy):
			if not tiles[i][j].walkable:
				return False
	return True


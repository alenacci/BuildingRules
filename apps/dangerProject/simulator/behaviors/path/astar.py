import copy
import heapq

class AStar:

	class ATile():
		def __init__(self,tile):
			self.x = tile.x
			self.y = tile.y
			self.walkable = tile.walkable
			self._in_open = False
			self._in_closed = False

		def __eq__(self, other):
			return self.x == other.x and self.y == other.y

		def __hash__(self):
			return hash(self.args)

		def __lt__(self, other):
			return self.f < other.f

		def __gt__(self, other):
			return self.f > other.f

		def __str__(self):
			w = " - walkable" if self.walkable else " - not walkwable"
			return "tile (" + str(self.x) + ", " + str(self.y) + ") " + w


	def __init__(self,grid,s_x,s_y,e_x,e_y, noCutEdges = True):
		self.width = grid.GRID_WIDTH
		self.height = grid.GRID_HEIGHT
		self.tiles =  [[AStar.ATile(grid.tiles[y][x]) for x in xrange(self.width)] for y in xrange(self.height)]
		self.s_x = s_x
		self.s_y = s_y
		self.e_x = e_x
		self.e_y = e_y
		self.startTile = self.tiles[s_x][s_y]
		self.endTile = self.tiles[e_x][e_y]
		self.noCutEdges = noCutEdges

		self.startTile.g = 0
		self.startTile.h = self._manhattanToEnd(s_x,s_y)
		self.startTile.f = self.startTile.g + self.startTile.h

		self.open_list = []
		heapq.heappush(self.open_list, self.startTile)
		self.closed_list = []


	def computePath(self):
		lowf = self._getLowerF()
		lowf = heapq.heappop(self.open_list)

		while lowf != self.endTile:
			self.closed_list.append(lowf)
			lowf._in_closed = True

			lowf._in_open = False
			expanded = self._expandTile(lowf)

			if len(self.open_list) != 0:
				lowf = heapq.heappop(self.open_list)
			else:
				return None
		return self._buildPath()

	def _getLowerF(self):
		return min(self.open_list)


	def _manhattanToEnd(self,x,y):
		return abs(self.e_x - x) + abs(self.e_y - y)

	def _expandTile(self,tile):

		for i in range(-1,2):
			for j in range(-1,2):

				if i == 0 and j == 0:
					continue

				x = tile.x + i
				y = tile.y + j

				#print "e- " + str(x) + " " + str(y)

				if x < 0 or y < 0 or \
					x >= self.width or y >= self.height:
					continue

				#diagonal
				if abs(i) + abs(j) > 1:
					g = 1.4
					#do not allow diagonal movement if it is on a corner
					if self.noCutEdges and \
						not self.tiles[tile.x + i][tile.y].walkable or \
						not self.tiles[tile.x][tile.y+j].walkable:
						continue
				else:
					g = 1.0
				#straight

				t = self.tiles[x][y]
				#print "exp "  +  str(t)

				if t.walkable and not t._in_closed:
					if not t._in_open:
						t.h = self._manhattanToEnd(t.x,t.y)
						t.g = tile.g + g
						t.f = t.h + t.g
						t.p = tile
						#Add an attribute to mark
						t._in_open = True
						heapq.heappush(self.open_list,t)
					elif t.g > tile.g + g:
						t.h = self._manhattanToEnd(t.x,t.y)
						t.g = tile.g + g
						t.f = t.h + t.g
						t.p = tile


	def _buildPath(self):
		c = self.endTile
		path = [c]

		while c != self.startTile:
			path.insert(0,c.p)
			c = c.p

		return path

	def _isInOpenList(self,t):
		return hasattr(t,'_in_open') and t._in_open

	def _isInClosedList(self,t):
		return hasattr(t,'_in_closed') and t._in_closed
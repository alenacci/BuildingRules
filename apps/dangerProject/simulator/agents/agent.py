from commons.point import Point

class Agent(object):

	def __init__(self):
		self.p = Point(0,0)
		self.current_action = None

	def setPosition(self,p):
		self.p = p.dup()

	@property
	def x(self):
		return self.p.x

	@x.setter
	def x(self,v):
		self.p.x = v

	@property
	def y(self):
		return self.p.y

	@y.setter
	def y(self,v):
		self.p.y = v

	def setCurrentAction(self,action):
		action.agent = self
		self.current_action = action

	def update(self):
		if self.current_action:
			self.current_action.update()
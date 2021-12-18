class Ray:

	def __init__(self, origin, direction):
		self.orig = origin
		self.dir = direction

	def at(self, t):
		return orig + t * dir
	
	def origin(self):
		return self.orig
	
	def direction(self):
		return self.dir
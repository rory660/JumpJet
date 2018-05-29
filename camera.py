class Camera:
	def __init__(self, width = 1280, height = 720, x = 0, y = 0):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.calculateEdgeLocations()

	def move(self, x, y):
		self.x = x
		self.y = y
		self.calculateEdgeLocations()

	def moveRelative(self, x, y):
		self.x += x
		self.y += y
		self.calculateEdgeLocations()

	def moveCenter(self, x, y):
		self.x = x - self.width / 2
		self.y = y - self. height / 2
		self.calculateEdgeLocations()

	def calculateEdgeLocations(self):
		self.right = self.x + self.width
		self.bottom = self.y + self.height
		self.center = (self.x + self.width / 2, self.y + self.height / 2)
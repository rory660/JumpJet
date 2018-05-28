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

	def calculateEdgeLocations(self):
		self.right = self.x + self.width
		self.bottom = self.y + self.height
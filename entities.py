import pygame

class Entity:
	def __init__(self, sprite, x, y):
		self.sprite = sprite
		self.width, self.height = sprite.get_size()
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

class Wall(Entity):
	def __init__(self, sprite, x, y):
		super().__init__(sprite, x, y)

class Hazard(Entity):
	def __init__(self, sprite, x, y):
		super().__init__(sprite, x, y)

class Entrance(Entity):
	def __init__(self, x, y):
		super().__init__(pygame.image.load("./other/entrance.png"), x, y)
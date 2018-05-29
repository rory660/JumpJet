import pygame
import os

def loadSpritesFromFolder(path):
	return [pygame.image.load(path + fileName) for fileName in os.listdir(path)]
sprites = {"walls":loadSpritesFromFolder("./walls/"), "hazards":loadSpritesFromFolder("./hazards/")}
class Entity:
	def __init__(self, sprite, x, y):
		self.sprite = sprite
		self.x = x
		self.y = y
		self.width, self.height = sprite.get_size()
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

	def setSprite(self, sprite):
		self.sprite = sprite
		self.width, self.height = sprite.get_size()
		self.calculateEdgeLocations()

class Wall(Entity):
	def __init__(self, spriteId, x, y):
		self.spriteId = spriteId
		super().__init__(sprites["walls"][spriteId], x, y)

class Hazard(Entity):
	def __init__(self, spriteId, x, y):
		self.spriteId = spriteId
		super().__init__(sprites["hazards"][spriteId], x, y)

class Entrance(Entity):
	def __init__(self, x, y):
		super().__init__(pygame.image.load("./other/entrance.png"), x, y)

class Exit(Entity):
	def __init__(self, x, y):
		super().__init__(pygame.image.load("./other/exit.png"), x, y)
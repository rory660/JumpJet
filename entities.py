import pygame

class Entity:
	def __init__(self, sprite, x, y):
		self.sprite = sprite
		self.width, self.height = sprite.get_size()
		self.x = x
		self.y = y
		self.right = x + self.width
		self.bottom = y + self.height

class Wall(Entity):
	def __init__(self, sprite, x, y):
		super().__init__(sprite, x, y)

class Hazard(Entity):
	def __init__(self, sprite, x, y):
		super().__init__(sprite, x, y)
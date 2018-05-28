import pygame
import os

class Renderer:
	def __init__(self):
		self.width = 500
		self.height = 500
		pygame.init()
		self.display = pygame.display.set_mode((self.width, self.height))
		self.sprites = {"walls":[loadSpritesFromFolder("./walls")], "hazards":[]}

	def loadSpritesFromFolder(self, path):
		return [pygame.image.load(path + fileName) for fileName in os.listdir(path)]

	def update(self):
		pygame.display.update()

class Map:
	def __init__(self):
		self.width = 1000
		self.height = 1000
		self.entities = {"walls":[], "hazards":[]}

class Entity:
	def __init__(self):

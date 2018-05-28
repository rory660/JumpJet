import pygame
import time
import os

class Renderer:
	def __init__(self, camera, gameMap):
		self.camera = camera
		pygame.init()
		self.display = pygame.display.set_mode((self.camera.width, self.camera.height))
		self.sprites = {"walls":self.loadSpritesFromFolder("./walls/"), "hazards":[]}
		self.currentTime = time.clock()
		self.maxFPS = 60
		self.map = gameMap

	def loadSpritesFromFolder(self, path):
		return [pygame.image.load(path + fileName) for fileName in os.listdir(path)]

	def update(self):
		self.display.fill((0,0,0))
		for wall in self.map.getWalls():
			relativeX = wall.x - self.camera.x
			relativeY = wall.y - self.camera.y
			self.display.blit(wall.sprite, (relativeX, relativeY))
		pygame.display.update()

		frameTime = time.clock() - self.currentTime
		if frameTime < 1000.0 / self.maxFPS:
			time.sleep((1000.0 / self.maxFPS - frameTime) / 1000.0)
		self.currentTime = time.clock()
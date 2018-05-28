import pygame
import time
import os


class Renderer:
	def __init__(self, camera, gameLevel, editorMode = False):
		self.editorMode = editorMode
		self.camera = camera
		pygame.init()
		self.display = pygame.display.set_mode((self.camera.width, self.camera.height))
		self.sprites = {"walls":self.loadSpritesFromFolder("./walls/"), "hazards":self.loadSpritesFromFolder("./hazards/")}
		self.currentTime = time.clock()
		self.maxFPS = 60
		self.level = gameLevel

	def loadSpritesFromFolder(self, path):
		return [pygame.image.load(path + fileName) for fileName in os.listdir(path)]

	def update(self, entitiesToDraw = []):
		self.display.fill((0,0,0))
		if self.editorMode:
			pygame.draw.rect(self.display, (0,150,0), pygame.Rect(-self.camera.x, -self.camera.y, self.level.width, self.level.height))
		

		for wall in self.level.getWalls():
			relativeX = wall.x - self.camera.x
			relativeY = wall.y - self.camera.y
			self.display.blit(wall.sprite, (relativeX, relativeY))
		for hazard in self.level.getHazards():
			relativeX = hazard.x - self.camera.x
			relativeY = hazard.y - self.camera.y
			self.display.blit(hazard.sprite, (relativeX, relativeY))

		for entity in entitiesToDraw:
			relativeX = entity.x - self.camera.x
			relativeY = entity.y - self.camera.y
			self.display.blit(entity.sprite, (relativeX, relativeY))
		if self.level.entrance != None:
			relativeX = self.level.entrance.x - self.camera.x
			relativeY = self.level.entrance.y - self.camera.y
			self.display.blit(self.level.entrance.sprite, (relativeX, relativeY))
		pygame.display.update()

		frameTime = time.clock() - self.currentTime
		if frameTime < 1000.0 / self.maxFPS:
			time.sleep((1000.0 / self.maxFPS - frameTime) / 1000.0)
		self.currentTime = time.clock()
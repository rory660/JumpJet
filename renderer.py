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
		self.frameTime = 0

	def loadSpritesFromFolder(self, path):
		return [pygame.image.load(path + fileName) for fileName in os.listdir(path)]

	def update(self, entitiesToDraw = []):
		self.display.fill((0,0,0))
		if self.editorMode:
			pygame.draw.rect(self.display, (0,150,0), pygame.Rect(-self.camera.x, -self.camera.y, self.level.width, self.level.height))

		for wall in self.level.getWalls():
			self.drawEntity(wall)
		for hazard in self.level.getHazards():
			self.drawEntity(hazard)

		for entity in entitiesToDraw:
			self.drawEntity(entity)

		if self.level.entrance != None:
			self.drawEntity(self.level.entrance)
		if self.level.exit != None:
			self.drawEntity(self.level.exit)

		if not self.editorMode:
			if self.level.player != None:
				self.drawEntity(self.level.player)
		pygame.display.update()

		self.frameTime = time.clock() - self.currentTime
		if self.frameTime < 1000.0 / self.maxFPS:
			time.sleep((1000.0 / self.maxFPS - self.frameTime) / 1000.0)
		self.currentTime = time.clock()

	def drawEntity(self, entity):
		relativeX = entity.x - self.camera.x
		relativeY = entity.y - self.camera.y
		if entity.currentAnimation != None:
			self.display.blit(entity.currentAnimation.getCurrentFrame(self.frameTime), (relativeX, relativeY))
		else:
			self.display.blit(entity.sprite, (relativeX, relativeY))
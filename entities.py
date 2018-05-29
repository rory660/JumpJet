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
		self.center = (self.x + self.width / 2, self.y + self.height / 2)

	def setSprite(self, sprite):
		self.sprite = sprite
		self.width, self.height = sprite.get_size()
		self.calculateEdgeLocations()

	def isCollidingWith(self, entity):
		if self.x < entity.right and self.right > entity.x:
			if self.y < entity.bottom and self.bottom > entity.y:
				return True

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

class Player(Entity):
	def __init__(self, parentLevel, x, y):
		super().__init__(pygame.image.load("./other/guy.png"), x, y)
		self.parentLevel = parentLevel
		self.speed = [0, 0]
		self.acceleration = [0, 0]
		self.inAir = False
		self.maxRunSpeed = 400
		self.runAcceleration = 3000
		self.airAcceleration = 1200
		self.slowdownRate = 2000
		self.maxAirSpeed = 1000
		self.running = 0
		self.jumping = False
		self.jumpTimer = 0.3
		self.gravity = 3000

	def calculateMovement(self, timeLength):
		if self.inAir and not self.jumping:
			self.jumpTimer = 0
		if self.jumpTimer > 0 and self.jumping:
			self.inAir = True
			self.speed[1] = -800
			self.jumpTimer -= timeLength
		if not self.inAir:
			self.jumpTimer = 0.3
			if self.speed[0] > 0 or self.running == 1 and self.speed[0] == 0:
				self.acceleration[0] = -self.slowdownRate
			if self.speed[0] < 0 or self.running == -1 and self.speed[0] == 0:
				self.acceleration[0] = self.slowdownRate

			if self.running != 0:
				self.acceleration[0] += self.running * self.runAcceleration
				self.speed[0] += self.acceleration[0] * timeLength
				if self.speed[0] < -self.maxRunSpeed:
					self.speed[0] = -self.maxRunSpeed
				elif self.speed[0] > self.maxRunSpeed:
					self.speed[0] = self.maxRunSpeed
			else:
				if self.speed[0] < 0:
					self.speed[0] += self.acceleration[0] * timeLength
					if self.speed[0] > 0:
						self.stop()
				elif self.speed[0] > 0:
					self.speed[0] += self.acceleration[0] * timeLength
					if self.speed[0] < 0:
						self.stop()
		else:
			if self.running > 0:
				self.acceleration[0] = self.airAcceleration
			elif self.running < 0:
				self.acceleration[0] = -self.airAcceleration
			else:
				self.acceleration[0] = 0
			self.speed[0] += self.acceleration[0] * timeLength
			if self.speed[0] > self.maxRunSpeed:
				self.speed[0] = self.maxRunSpeed
			elif self.speed[0] < -self.maxRunSpeed:
				self.speed[0] = -self.maxRunSpeed

		self.acceleration[1] = self.gravity
		self.speed[1] += self.acceleration[1] * timeLength
		if self.speed[1] > self.maxAirSpeed:
			self.speed[1] = self.maxAirSpeed
		elif self.speed[1] < -self.maxAirSpeed:
			self.speed[1] = -self.maxAirSpeed

		self.moveRelative(self.speed[0] * timeLength, self.speed[1] * timeLength)
		self.running = 0

	def runLeft(self):
		self.running = -1
	def runRight(self):
		self.running = 1

	def stop(self, horizontal = True, vertical = True):
		if horizontal:
			self.speed[0] = 0
			self.acceleration[0] = 0
		if vertical:
			self.speed[0] = 0
			self.acceleration[0] = 0

	def moveRelative(self, x, y):
		self.x += x
		self.x = int(self.x)
		self.calculateEdgeLocations()
		checkingCollision = True
		while checkingCollision:
			checkingCollision = False
			for wall in self.parentLevel.getWalls():
				if self.isCollidingWith(wall):
					self.speed[0] = 0
					checkingCollision = True
					if x < 0:
						self.x = wall.right
					elif x > 0:
						self.x = wall.x - self.width
					self.calculateEdgeLocations()
					
		self.y += y
		self.y = int(self.y)
		self.calculateEdgeLocations()
		checkingCollision = True
		self.inAir = True
		while checkingCollision:
			checkingCollision = False
			for wall in self.parentLevel.getWalls():
				if self.isCollidingWith(wall):
					self.speed[1] = 0
					checkingCollision = True
					if y < 0:
						self.y = wall.bottom
						self.jumpTimer = 0
					elif y > 0:
						self.y = wall.y - self.height
						self.inAir = False
					self.calculateEdgeLocations()

	def isOutOfBounds(self):
		return self.x > self.parentLevel.width or self.y > self.parentLevel.height or self.right < 0 or self.bottom < 0

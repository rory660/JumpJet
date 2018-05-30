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
		self.inAir = False

		self.runAcceleration = 3000
		self.running = 0
		self.jumping = False
		

		self.runAcceleration = 1000
		self.boostSpeed = 1000
		self.runSpeed = 400
		self.fallSpeed = 0
		self.hBoosting = 0
		self.vBoosting = 0
		self.jumpSpeed = 800
		self.boostDistance = 50

		self.airHAcceleration = 1000
		self.hAcceleration = 2000
		self.vAcceleration = 3000


	def calculateMovement(self, timeLength):
		print(self.inAir)
		self.hDesiredSpeed = 0
		self.vDesiredSpeed = 1000
		if self.running != 0:
			self.hDesiredSpeed = self.runSpeed * self.running
			if not self.inAir:
				if self.speed[0] < self.hDesiredSpeed:
					self.speed[0] += self.runAcceleration * timeLength
				elif self.speed[0] > self.hDesiredSpeed:
					self.speed[0] -= self.runAcceleration * timeLength

		if self.hBoosting != 0:
			self.speed[0] = self.hBoosting * self.boostSpeed

		if self.vBoosting != 0:
			self.speed[1] = self.vBoosting * self.boostSpeed

		if self.jumping:
			self.speed[1] = -self.jumpSpeed

		hAccel = self.hAcceleration
		if self.inAir:
			hAccel = self.airHAcceleration
		if self.speed[0] < self.hDesiredSpeed:
			self.speed[0] += hAccel * timeLength
			if self.speed[0] > self.hDesiredSpeed:
				self.speed[0] = self.hDesiredSpeed
		elif self.speed[0] > self.hDesiredSpeed:
			self.speed[0] -= hAccel * timeLength
			if self.speed[0] < self.hDesiredSpeed:
				self.speed[0] = self.hDesiredSpeed

		if self.speed[1] < self.vDesiredSpeed:
			self.speed[1] += self.vAcceleration * timeLength
			if self.speed[1] > self.vDesiredSpeed:
				self.speed[1] = self.vDesiredSpeed
		elif self.speed[1] > self.vDesiredSpeed:
			self.speed[1] -= self.vAcceleration * timeLength
			if self.speed[1] < self.vDesiredSpeed:
				self.speed[1] = self.vDesiredSpeed

		

		xMove = self.speed[0] * timeLength
		yMove = self.speed[1] * timeLength

		if self.hBoosting != 0:
			xMove += self.boostDistance * self.hBoosting
		elif self.vBoosting != 0:
			yMove += self.boostDistance * self.vBoosting

		self.running = 0
		self.hBoosting = 0
		self.vBoosting = 0
		self.jumping = False

		self.moveRelative(xMove, yMove)

	def runLeft(self):
		self.running = -1
	def runRight(self):
		self.running = 1

	def boostLeft(self):
		self.hBoosting = -1

	def boostRight(self):
		self.hBoosting = 1

	def boostDown(self):
		self.vBoosting = 1

	def boostUp(self):
		self.vBoosting = -1

	def stop(self, horizontal = True, vertical = True):
		if horizontal:
			self.speed[0] = 0
		if vertical:
			self.speed[1] = 0

	def moveRelative(self, x, y):
		self.x += x
		self.x = int(self.x)
		self.calculateEdgeLocations()
		checkingCollision = True
		while checkingCollision:
			checkingCollision = False
			for wall in self.parentLevel.getWalls():
				if self.isCollidingWith(wall):
					self.stop(vertical = False)
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
					self.stop(horizontal = False)
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

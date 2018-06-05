import pygame
import os
import animation
import math

SHAPE_SQUARE = 0
SHAPE_CIRCLE = 1
SHAPE_FANCY = 2

def loadSpritesFromFolder(path):
	return [pygame.image.load(path + fileName) for fileName in os.listdir(path)]
sprites = {"walls":loadSpritesFromFolder("./walls/"), "hazards":loadSpritesFromFolder("./hazards/")}
hazardAnimations = [loadSpritesFromFolder("./hazardAnimations/" + directory + "/") for directory in os.listdir("./hazardAnimations")]
class Entity:
	def __init__(self, sprite, x, y, shape = SHAPE_SQUARE, movingOnPath = False):
		self.sprite = sprite
		self.currentAnimation = None
		self.shape = shape
		self.movingOnPath = movingOnPath
		self.pathMoveDir = [0,0]
		self.path = []
		self.movingTarget = 1
		self.movingSpeed = 300
		self.x = x
		self.y = y
		self.pathInit = True
		self.lastMoveDistance = 0
		self.width, self.height = sprite.get_size()
		self.calculateEdgeLocations()

	def move(self, x, y):
		self.x = x
		self.y = y
		self.calculateEdgeLocations()

	def setMovingPath(self, start, finish, speed = 300):
		self.path = [start, finish]
		self.movingOnPath = True
		self.movingSpeed = speed


	def moveOnPath(self, timeLength):
		if self.pathInit == True:
			self.x = self.path[0][0]
			self.y = self.path[0][1]
			self.pathInit = False
		target = self.path[self.movingTarget]
		oldX = self.x
		oldY = self.y
		xDistance = target[0] - self.x
		yDistance = target[1] - self.y
		
		xMoveAmount = 0
		yMoveAmount = 0
		if abs(xDistance) + abs(yDistance) != 0:
			xMoveAmount = round(xDistance / (abs(xDistance) + abs(yDistance)) * self.movingSpeed * timeLength)
			self.lastMoveDistance = xMoveAmount
			yMoveAmount = round(yDistance / (abs(xDistance) + abs(yDistance)) * self.movingSpeed * timeLength)


		if xMoveAmount > 0:
			self.pathMoveDir[0] = 1
		elif xMoveAmount < 0:
			self.pathMoveDir[0] = -1
		if yMoveAmount > 0:
			self.pathMoveDir[1] = 1
		elif yMoveAmount < 0:
			self.pathMoveDir[1] = -1
		self.moveRelative(xMoveAmount, yMoveAmount)

		if self.pathMoveDir[0] != 0:
			if (oldX < target[0] and self.x >= target[0]) or (oldX > target[0] and self.x <= target[0]):
				if self.movingTarget == 1:
					self.movingTarget = 0
				else:
					self.movingTarget = 1
		elif self.pathMoveDir[1] != 0:
			if (oldY < target[1] and self.y >= target[1]) or (oldY > target[1] and self.y <= target[1]) or (xMoveAmount == 0 and yMoveAmount == 0):
				if self.movingTarget == 1:
					self.movingTarget = 0
				else:
					self.movingTarget = 1

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
		if self.shape == SHAPE_FANCY and entity.shape == SHAPE_FANCY:
			mask1 = pygame.mask.from_surface(self.getCurrentSprite())
			mask2 = pygame.mask.from_surface(entity.getCurrentSprite())
			if mask1.overlap(mask2, (entity.x - self.x, entity.y - self.y)) != None:
				return True
			return False
		if self.x < entity.right and self.right > entity.x:
			if self.y < entity.bottom and self.bottom > entity.y:
				if self.shape == SHAPE_CIRCLE and entity.shape == SHAPE_CIRCLE:
					if ((self.center[0] - entity.center[0])**2 + (self.center[1] - entity.center[1])**2)**0.5 <=self.width / 2 + entity.width / 2:
						return True
				else:
					return True
		return False

	def setAnimation(self, animation):
		if self.currentAnimation != None:
			self.currentAnimation.reset()
		self.currentAnimation = animation

	def isClicked(self, mouseX, mouseY):
		return mouseX >= self.x and mouseX <= self.right and mouseY >= self.y and mouseY <= self.bottom

	def getCurrentSprite(self):
		if self.currentAnimation != None:
			return self.currentAnimation.getCurrentFrame(0)
		return self.sprite

class Wall(Entity):
	def __init__(self, spriteId, x, y, shape = SHAPE_SQUARE):
		self.spriteId = spriteId
		super().__init__(sprites["walls"][spriteId], x, y)

class Hazard(Entity):
	def __init__(self, spriteId, x, y):
		self.spriteId = spriteId
		super().__init__(sprites["hazards"][spriteId], x, y, shape = SHAPE_FANCY)
		if hazardAnimations[spriteId] != []:
			anim = animation.Animation(hazardAnimations[spriteId], [0.2 for x in hazardAnimations[spriteId]])
			self.setAnimation(anim)

class Entrance(Entity):
	def __init__(self, x, y):
		super().__init__(pygame.image.load("./other/entrance.png"), x, y)

class Exit(Entity):
	def __init__(self, x, y):
		super().__init__(pygame.image.load("./other/exit.png"), x, y)

class Player(Entity):
	def __init__(self, parentLevel, x, y):
		super().__init__(pygame.image.load("./player/run1.png"), x, y, shape = SHAPE_FANCY)
		self.parentLevel = parentLevel
		self.speed = [0, 0]
		self.inAir = False

		self.runAcceleration = 3000
		self.running = 0
		self.jumping = False
		

		self.runAcceleration = 1000
		self.runSpeed = 400
		self.fallSpeed = 0
		self.jumpSpeed = 1000

		self.airHAcceleration = 1000
		self.hAcceleration = 2000
		self.vAcceleration = 3000

		self.runFrames = [pygame.image.load("./player/run" + str(x) + ".png") for x in range(1,7)]
		self.runLeftFrames = [pygame.transform.flip(img, True, False) for img in self.runFrames]
		self.leftAnimation = animation.Animation(self.runLeftFrames, [0.02 for x in range(1,7)])
		self.rightAnimation = animation.Animation(self.runFrames, [0.02 for x in range(1,7)])


	def calculateMovement(self, timeLength):
		self.hDesiredSpeed = 0
		self.vDesiredSpeed = 1000
		if self.running != 0:
			self.hDesiredSpeed = self.runSpeed * self.running
			if not self.inAir:
				if self.speed[0] < self.hDesiredSpeed:
					self.speed[0] += self.runAcceleration * timeLength
				elif self.speed[0] > self.hDesiredSpeed:
					self.speed[0] -= self.runAcceleration * timeLength

		elif self.currentAnimation != None:
			self.sprite = self.currentAnimation.getCurrentFrame(0)
			self.currentAnimation = None

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

		self.running = 0
		self.jumping = False

		self.moveRelative(xMove, yMove)

	def runLeft(self):
		self.running = -1
		self.currentAnimation = self.leftAnimation
	def runRight(self):
		self.running = 1
		self.currentAnimation = self.rightAnimation

	def jump(self):
		if not self.inAir:
			self.jumping = True

	def stop(self, horizontal = True, vertical = True):
		if horizontal:
			self.speed[0] = 0
		if vertical:
			self.speed[1] = 0

	def moveRelative(self, x, y, checkColX = True, checkColY = True):
		self.x += x
		self.x = int(self.x)
		self.calculateEdgeLocations()
		checkingCollision = True
		while checkingCollision and checkColX:
			checkingCollision = False
			for wall in self.parentLevel.getWalls():
				if self.isCollidingWith(wall):
					self.stop(vertical = False)
					checkingCollision = True
					if wall.movingOnPath and wall.pathMoveDir[0] != 0:
						if self.center[0] > wall.center[0]:
							self.x += 1
						elif self.center[0] < wall.center[0]:
							self.x -= 1
					else:
						if x < 0:
							self.x = wall.right
						elif x > 0:
							self.x = wall.x - self.width
					
					self.calculateEdgeLocations()
					
		self.y += y
		self.y = int(self.y)
		self.calculateEdgeLocations()
		
		if checkColY:
			checkingCollision = True
			self.inAir = True
		while checkingCollision and checkColY:
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
						if wall.lastMoveDistance != 0:
							self.moveRelative(wall.lastMoveDistance, 0, checkColY = False)
					self.calculateEdgeLocations()		

	def isOutOfBounds(self):
		return self.x > self.parentLevel.width or self.y > self.parentLevel.height or self.right < 0 or self.bottom < 0

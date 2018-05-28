import pygame
import os
import time

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

class Editor:
	def __init__(self, gameMap = None):
		
		if gameMap != None:
			self.map = gameMap
		else:
			self.map = Map()
			
		self.camera = Camera()
		self.renderer = Renderer(self.camera, self.map)
		self.running = True
		self.mouseDown = False
		self.mouseX = 0
		self.mouseY = 0
		self.absMouseX = 0
		self.absMouseY = 0
		self.clicked = False
		self.keysDown = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False}
		self.mainLoop()

	def getInput(self):
		self.mouseX, self.mouseY = pygame.mouse.get_pos()
		self.absMouseX = self.mouseX + self.camera.x
		self.absMouseY = self.mouseY + self.camera.y
		self.clicked = False
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.mouseDown = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouseDown = False
				self.clicked = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.keysDown["esc"] = True
				elif event.key == pygame.K_w:
					self.keysDown["w"] = True
				elif event.key == pygame.K_a:
					self.keysDown["a"] = True
				elif event.key == pygame.K_s:
					self.keysDown["s"] = True
				elif event.key == pygame.K_d:
					self.keysDown["d"] = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.keysDown["esc"] = False
				elif event.key == pygame.K_w:
					self.keysDown["w"] = False
				elif event.key == pygame.K_a:
					self.keysDown["a"] = False
				elif event.key == pygame.K_s:
					self.keysDown["s"] = False
				elif event.key == pygame.K_d:
					self.keysDown["d"] = False


	def mainLoop(self):
		while(self.running):
			self.getInput()
			if self.keysDown["esc"]:
				self.running = False
			if self.keysDown["w"]:
				self.camera.y -= 5
			if self.keysDown["a"]:
				self.camera.x -= 5
			if self.keysDown["s"]:
				self.camera.y += 5
			if self.keysDown["d"]:
				self.camera.x += 5

			if self.clicked:
				self.map.addEntity(Wall(self.renderer.sprites["walls"][0], self.absMouseX, self.absMouseY))
			self.renderer.update()

class Map:
	def __init__(self):
		self.width = 1000
		self.height = 1000
		self.entities = {"walls":[], "hazards":[]}

	def addEntity(self, entity):
		if isinstance(entity, Wall):
			self.entities["walls"].append(entity)
		elif isinstance(entity, Hazard):
			self.entities["hazards"].append(entity)

	def getWalls(self):
		return self.entities["walls"]

	def getHazards(self):
		return self.entities["hazards"]

class Camera:
	def __init__(self, width = 500, height = 500, x = 0, y = 0):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.calculateEdgeLocations()

	def move(self, x, y):
		self.x = x
		self.y = y

	def moveRelative(self, x, y):
		self.x += x
		self.y += y

	def calculateEdgeLocations(self):
		self.right = self.x + self.width
		self.bottom = self.y + self.height


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

editor = Editor()
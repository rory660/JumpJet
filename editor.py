import pygame
import renderer
import level
import camera
import entities

class Editor:
	def __init__(self, gameLevel = None):
		
		if gameLevel != None:
			self.level = gameLevel
		else:
			self.level = level.Level()
			
		self.camera = camera.Camera()
		self.renderer = renderer.Renderer(self.camera, self.level)
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
				self.level.addEntity(entities.Wall(self.renderer.sprites["walls"][0], self.absMouseX, self.absMouseY))
			self.renderer.update()








editor = Editor()
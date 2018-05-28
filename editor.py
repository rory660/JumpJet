import pygame
import renderer
import level
import camera
import entities
import time

MODE_WALLS = 0
MODE_HAZARDS = 1
MODE_ENTRANCE = 2
MODES = 3
class Editor:
	def __init__(self, gameLevel = None):
		
		if gameLevel != None:
			self.level = gameLevel
		else:
			self.level = level.Level()
			
		self.camera = camera.Camera()
		self.renderer = renderer.Renderer(self.camera, self.level, editorMode = True)
		self.running = True
		self.mouseDown = False
		self.mouseX = 0
		self.mouseY = 0
		self.absMouseX = 0
		self.absMouseY = 0
		self.clicked = False
		self.keysDown = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False}
		self.keysPressed = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False}
		self.currentTime = time.clock()
		self.timePassed = 0
		self.mode = MODE_WALLS
		self.idSelected = 0
		self.mainLoop()

	def getInput(self):
		self.mouseX, self.mouseY = pygame.mouse.get_pos()
		self.absMouseX = self.mouseX + self.camera.x
		self.absMouseY = self.mouseY + self.camera.y
		self.clicked = False
		self.keysPressed = dict.fromkeys(self.keysPressed, False)
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
				elif event.key == pygame.K_q:
					self.keysDown["q"] = True
				elif event.key == pygame.K_e:
					self.keysDown["e"] = True
				elif event.key == pygame.K_z:
					self.keysDown["z"] = True
				elif event.key == pygame.K_x:
					self.keysDown["x"] = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.keysDown["esc"] = False
					self.keysPressed["esc"] = True
				elif event.key == pygame.K_w:
					self.keysDown["w"] = False
					self.keysPressed["w"] = True
				elif event.key == pygame.K_a:
					self.keysDown["a"] = False
					self.keysPressed["a"] = True
				elif event.key == pygame.K_s:
					self.keysDown["s"] = False
					self.keysPressed["s"] = True
				elif event.key == pygame.K_d:
					self.keysDown["d"] = False
					self.keysPressed["d"] = True
				elif event.key == pygame.K_q:
					self.keysDown["q"] = False
					self.keysPressed["q"] = True
				elif event.key == pygame.K_e:
					self.keysDown["e"] = False
					self.keysPressed["e"] = True
				elif event.key == pygame.K_z:
					self.keysDown["z"] = False
					self.keysPressed["z"] = True
				elif event.key == pygame.K_x:
					self.keysDown["x"] = False
					self.keysPressed["x"] = True


	def mainLoop(self):
		selectedEntity = entities.Wall(self.renderer.sprites["walls"][self.idSelected], int(self.absMouseX/10)*10, int(self.absMouseY/10)*10)
		while(self.running):
			refreshEntity = False
			self.getInput()
			if self.keysDown["esc"]:
				self.running = False
			if self.keysDown["w"]:
				self.camera.moveRelative(0, -500 * self.timePassed)
			if self.keysDown["a"]:
				self.camera.moveRelative(-500 * self.timePassed, 0)
			if self.keysDown["s"]:
				self.camera.moveRelative(0, 500 * self.timePassed)
			if self.keysDown["d"]:
				self.camera.moveRelative(500 * self.timePassed, 0)
			if self.keysPressed["q"]:
				if self.mode == MODE_WALLS:
					if self.idSelected > 0:
						self.idSelected -= 1
						refreshEntity = True
				elif self.mode == MODE_HAZARDS:
					if self.idSelected > 0:
						self.idSelected -= 1
						refreshEntity = True
			if self.keysPressed["e"]:
				if self.mode == MODE_WALLS:
					if self.idSelected < len(self.renderer.sprites["walls"]) - 1:
						self.idSelected += 1
						refreshEntity = True
				elif self.mode == MODE_HAZARDS:
					if self.idSelected < len(self.renderer.sprites["hazards"]) - 1:
						self.idSelected += 1
						refreshEntity = True

			if self.keysPressed["z"]:
				if self.mode > 0:
					self.mode -= 1
					self.idSelected = 0
					refreshEntity = True
			if self.keysPressed["x"]:
				if self.mode < MODES - 1:
					self.mode += 1
					self.idSelected = 0
					refreshEntity = True

			if refreshEntity:
				if self.mode == MODE_WALLS:
					selectedEntity = entities.Wall(self.renderer.sprites["walls"][self.idSelected], int(self.absMouseX/10)*10, int(self.absMouseY/10)*10)
				elif self.mode == MODE_HAZARDS:
					selectedEntity = entities.Hazard(self.renderer.sprites["hazards"][self.idSelected], int(self.absMouseX/10)*10, int(self.absMouseY/10)*10)
				elif self.mode == MODE_ENTRANCE:
					selectedEntity = entities.Entrance(int(self.absMouseX/10)*10, int(self.absMouseY/10)*10)
			selectedEntity.move(int(self.absMouseX/10)*10, int(self.absMouseY/10)*10)

			if self.clicked:
				if self.mode == MODE_WALLS:
					self.level.addEntity(entities.Wall(self.renderer.sprites["walls"][self.idSelected], int(self.absMouseX/10)*10, int(self.absMouseY/10)*10))
				elif self.mode == MODE_HAZARDS:
					self.level.addEntity(entities.Hazard(self.renderer.sprites["hazards"][self.idSelected], int(self.absMouseX/10)*10, int(self.absMouseY/10)*10))
				elif self.mode == MODE_ENTRANCE:
					self.level.entrance = entities.Entrance(int(self.absMouseX/10)*10, int(self.absMouseY/10)*10)
			self.renderer.update([selectedEntity])
			self.timePassed = time.clock() - float(self.currentTime)
			self.currentTime = time.clock()

editor = Editor()
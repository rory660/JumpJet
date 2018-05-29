import pygame
import renderer
import level
import camera
import entities
import time
import saveManager

class Game:
	def __init__(self):
		self.saveManager = saveManager.SaveManager()
		self.level = self.saveManager.loadLevel(int(input("Enter level id:\n> ")))
			
		self.camera = camera.Camera()
		self.renderer = renderer.Renderer(self.camera, self.level, editorMode = False)
		self.running = True
		self.mouseDown = False
		self.mouseX = 0
		self.mouseY = 0
		self.absMouseX = 0
		self.absMouseY = 0
		self.clicked = False
		self.keysDown = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False, "ctrl" : False, "space" : False}
		self.keysPressed = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False, "ctrl" : False, "space" : False}
		self.currentTime = time.clock()
		self.timePassed = 0
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
				elif event.key == pygame.K_LCTRL:
					self.keysDown["ctrl"] = True
				elif event.key == pygame.K_SPACE:
					self.keysDown["space"] = True

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
				elif event.key == pygame.K_LCTRL:
					self.keysDown["ctrl"] = False
					self.keysPressed["ctrl"] = True
				elif event.key == pygame.K_SPACE:
					self.keysDown["space"] = False
					self.keysPressed["space"] = True

	def mainLoop(self):
		if self.level.player == None:
			self.level.player = entities.Player(self.level, self.level.entrance.x, self.level.entrance.y - 80)
		while(self.running):
			self.getInput()
			if self.keysDown["esc"]:
				self.running = False

			if self.keysDown["a"]:
				self.level.player.runLeft()

			if self.keysDown["d"]:
				self.level.player.runRight()
			if self.keysDown["space"]:
				self.level.player.jumping = True
			else:
				self.level.player.jumping = False

			
			

			self.level.player.calculateMovement(self.timePassed)
			if self.level.player.isOutOfBounds():
				self.level.player.move(self.level.entrance.x, self.level.entrance.y - 80)
			self.camera.moveCenter(self.level.player.center[0], self.level.player.center[1])
			if self.camera.x < 0:
				self.camera.x = 0
			if self.camera.y < 0:
				self.camera.y = 0
			if self.camera.right > self.level.width:
				self.camera.x = self.level.width - self.camera.width
			if self.camera.bottom > self.level.height:
				self.camera.y = self.level.height - self.camera.height
			self.renderer.update()
			self.timePassed = time.clock() - float(self.currentTime)
			self.currentTime = time.clock()


game = Game()
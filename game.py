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
		self.levelID = int(input("Enter level id:\n> "))
		self.level = self.saveManager.loadLevel(self.levelID)
			
		self.camera = camera.Camera()
		self.renderer = renderer.Renderer(self.camera, self.level, editorMode = False)
		self.running = True
		self.mouseDown = False
		self.mouseX = 0
		self.mouseY = 0
		self.absMouseX = 0
		self.absMouseY = 0
		self.clicked = False
		self.keysDown = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False, "ctrl" : False, "space" : False, "left" : False, "right" : False, "up" : False, "down" : False}
		self.keysPressed = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False, "ctrl" : False, "space" : False, "left" : False, "right" : False, "up" : False, "down" : False}
		self.keysPressedDown = {"esc" : False, "w" : False, "a" : False, "s" : False, "d" : False, "q" : False, "e" : False, "z" : False, "x" : False, "ctrl" : False, "space" : False, "left" : False, "right" : False, "up" : False, "down" : False}
		self.currentTime = time.clock()
		self.timePassed = 0
		self.mainLoop()

	def getInput(self):
		self.mouseX, self.mouseY = pygame.mouse.get_pos()
		self.absMouseX = self.mouseX + self.camera.x
		self.absMouseY = self.mouseY + self.camera.y
		self.clicked = False
		self.keysPressed = dict.fromkeys(self.keysPressed, False)
		self.keysPressedDown = dict.fromkeys(self.keysPressed, False)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.mouseDown = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouseDown = False
				self.clicked = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.keysDown["esc"] = True
					self.keysPressedDown["esc"] = True
				elif event.key == pygame.K_w:
					self.keysDown["w"] = True
					self.keysPressedDown["w"] = True
				elif event.key == pygame.K_a:
					self.keysDown["a"] = True
					self.keysPressedDown["a"] = True
				elif event.key == pygame.K_s:
					self.keysDown["s"] = True
					self.keysPressedDown["s"] = True
				elif event.key == pygame.K_d:
					self.keysDown["d"] = True
					self.keysPressedDown["d"] = True
				elif event.key == pygame.K_q:
					self.keysDown["q"] = True
					self.keysPressedDown["q"] = True
				elif event.key == pygame.K_e:
					self.keysDown["e"] = True
					self.keysPressedDown["e"] = True
				elif event.key == pygame.K_z:
					self.keysDown["z"] = True
					self.keysPressedDown["z"] = True
				elif event.key == pygame.K_x:
					self.keysDown["x"] = True
					self.keysPressedDown["x"] = True
				elif event.key == pygame.K_LCTRL:
					self.keysDown["ctrl"] = True
					self.keysPressedDown["ctrl"] = True
				elif event.key == pygame.K_SPACE:
					self.keysDown["space"] = True
					self.keysPressedDown["space"] = True
				elif event.key == pygame.K_UP:
					self.keysDown["up"] = True
					self.keysPressedDown["up"] = True
				elif event.key == pygame.K_DOWN:
					self.keysDown["down"] = True
					self.keysPressedDown["down"] = True
				elif event.key == pygame.K_LEFT:
					self.keysDown["left"] = True
					self.keysPressedDown["left"] = True
				elif event.key == pygame.K_RIGHT:
					self.keysDown["right"] = True
					self.keysPressedDown["right"] = True

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
				elif event.key == pygame.K_UP:
					self.keysDown["up"] = False
					self.keysPressed["up"] = True
				elif event.key == pygame.K_DOWN:
					self.keysDown["down"] = False
					self.keysPressed["down"] = True
				elif event.key == pygame.K_LEFT:
					self.keysDown["left"] = False
					self.keysPressed["left"] = True
				elif event.key == pygame.K_RIGHT:
					self.keysDown["right"] = False
					self.keysPressed["right"] = True

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
			if self.keysPressedDown["space"]:
				self.level.player.jump()

			if self.keysPressedDown["left"]:
				self.level.player.boostLeft()
			if self.keysPressedDown["right"]:
				self.level.player.boostRight()
			if self.keysPressedDown["up"]:
				self.level.player.boostUp()
			if self.keysPressedDown["down"]:
				self.level.player.boostDown()

			
			

			for hazard in self.level.entities["hazards"]:
				if hazard.movingOnPath:
					hazard.moveOnPath(self.timePassed)
			for wall in self.level.entities["walls"]:
				if wall.movingOnPath:
					wall.moveOnPath(self.timePassed)
					
			self.level.player.calculateMovement(self.timePassed)
			for hazard in self.level.entities["hazards"]:
				if self.level.player.isCollidingWith(hazard):
					self.respawnPlayer()
			if self.level.player.isOutOfBounds():
				self.respawnPlayer()
			if self.level.player.isCollidingWith(self.level.exit):
				self.levelID += 1
				self.level = self.saveManager.loadLevel(self.levelID)
				self.renderer.level = self.level
				self.level.player = entities.Player(self.level, self.level.entrance.x, self.level.entrance.y - 80)
			self.camera.moveCenter(self.level.player.center[0], self.level.player.center[1])
			if self.camera.width >= self.level.width:
				self.camera.moveCenter(self.level.width/2, self.camera.y + self.camera.height / 2)
			else:
				if self.camera.x < 0:
					self.camera.x = 0
				elif self.camera.right > self.level.width:
					self.camera.x = self.level.width - self.camera.width
			if self.camera.height >= self.level.height:
				self.camera.moveCenter(self.camera.x + self.camera.width / 2, self.level.height/2)
			else:
				if self.camera.y < 0:
					self.camera.y = 0
				elif self.camera.bottom > self.level.height:
					self.camera.y = self.level.height - self.camera.height
			self.renderer.update()
			self.timePassed = time.clock() - float(self.currentTime)
			self.currentTime = time.clock()

	def respawnPlayer(self):
		self.level.player.stop()
		self.level.player.move(self.level.entrance.x, self.level.entrance.y - 80)


game = Game()
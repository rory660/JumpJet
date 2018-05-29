import os
import level
import entities


MODE_DIM = 0
MODE_ENTS = 1

class SaveManager:
	def __init__(self):
		self.levelDirectory = "./levels/"
	def saveLevel(self, level, overwrite = True):
		if level.id == None or not overwrite:
			level.id = len([file for file in os.listdir(self.levelDirectory)])
		with open(self.levelDirectory + str(level.id) + ".level", "w") as levelFile:
			levelFile.write("")
		with open(self.levelDirectory + str(level.id) + ".level", "a") as levelFile:
			levelFile.write("dim:\n" + str(level.width) + "," + str(level.height) + "\n")
			levelFile.write("ents:\n")
			for wall in level.entities["walls"]:
				levelFile.write("wall," + str(wall.spriteId) + "," + str(wall.x) + "," + str(wall.y) + "\n")
			for hazard in level.entities["hazards"]:
				levelFile.write("hazard," + str(hazard.spriteId) + "," + str(hazard.x) + "," + str(hazard.y) + "\n")
			if not level.entrance == None:
				levelFile.write("entrance," + str(level.entrance.x) + "," + str(level.entrance.y) + "\n")
			if not level.exit == None:
				levelFile.write("exit," + str(level.exit.x) + "," + str(level.exit.y) + "\n")

	def loadLevel(self, levelId):
		loadedLevel = level.Level()
		if levelId >= len([file for file in os.listdir(self.levelDirectory)]):
			return loadedLevel
		else:
			loadedLevel.id = levelId
			with open(self.levelDirectory + str(levelId) + ".level", "r") as levelFile:
				readMode = MODE_DIM
				for line in levelFile:
					line = line.replace("\n", "")
					if not line == "":
						if "dim:" in line:
							readMode = MODE_DIM
							continue
						if "ents:" in line:
							readMode = MODE_ENTS
							continue
						if readMode == MODE_DIM:
							dims = [int(dim) for dim in line.split(",")]
							loadedLevel.width = dims[0]
							loadedLevel.height = dims[1]
						elif readMode == MODE_ENTS:
							entInfo = line.split(",")
							if entInfo[0] == "wall":
								loadedLevel.addEntity(entities.Wall(int(entInfo[1]), int(entInfo[2]), int(entInfo[3])))
							elif entInfo[0] == "hazard":
							 	loadedLevel.addEntity(entities.Hazard(int(entInfo[1]), int(entInfo[2]), int(entInfo[3])))
							elif entInfo[0] == "entrance":
							 	loadedLevel.entrance = entities.Entrance(int(entInfo[1]), int(entInfo[2]))
							elif entInfo[0] == "exit":
							 	loadedLevel.exit = entities.Exit(int(entInfo[1]), int(entInfo[2]))
		return loadedLevel
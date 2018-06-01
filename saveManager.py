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
				levelFile.write("wall," + str(wall.spriteId) + "," + str(wall.x) + "," + str(wall.y))
				if wall.movingOnPath:
					levelFile.write(",path," + str(wall.path[0][0]) + "," + str(wall.path[0][1]) + "," + str(wall.path[1][0]) + "," + str(wall.path[1][1]))
				levelFile.write("\n")
			for hazard in level.entities["hazards"]:
				levelFile.write("hazard," + str(hazard.spriteId) + "," + str(hazard.x) + "," + str(hazard.y))
				if hazard.movingOnPath:
					levelFile.write(",path," + str(hazard.path[0][0]) + "," + str(hazard.path[0][1]) + "," + str(hazard.path[1][0]) + "," + str(hazard.path[1][1]))
				levelFile.write("\n")
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
								ent = entities.Wall(int(entInfo[1]), int(entInfo[2]), int(entInfo[3]))
								if "path" in entInfo:
									ent.setMovingPath((int(entInfo[5]), int(entInfo[6])), (int(entInfo[7]), int(entInfo[8])))
								loadedLevel.addEntity(ent)
							elif entInfo[0] == "hazard":
								ent = entities.Hazard(int(entInfo[1]), int(entInfo[2]), int(entInfo[3]))
								if "path" in entInfo:
									ent.setMovingPath((int(entInfo[5]), int(entInfo[6])), (int(entInfo[7]), int(entInfo[8])))
								loadedLevel.addEntity(ent)
							elif entInfo[0] == "entrance":
							 	loadedLevel.entrance = entities.Entrance(int(entInfo[1]), int(entInfo[2]))
							elif entInfo[0] == "exit":
							 	loadedLevel.exit = entities.Exit(int(entInfo[1]), int(entInfo[2]))
		return loadedLevel
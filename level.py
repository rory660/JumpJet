import entities

class Level:
	def __init__(self):
		self.width = 1000
		self.height = 1000
		self.entities = {"walls":[], "hazards":[]}

	def addEntity(self, entity):
		if isinstance(entity, entities.Wall):
			self.entities["walls"].append(entity)
		elif isinstance(entity, entities.Hazard):
			self.entities["hazards"].append(entity)

	def getWalls(self):
		return self.entities["walls"]

	def getHazards(self):
		return self.entities["hazards"]
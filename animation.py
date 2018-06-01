
class Animation:
	def __init__(self, frames = [], delays = []):
		self.frames = frames
		self.delays = delays
		self.currentFrameIndex = 0
		self.time = 0

	def addFrame(self, frame, delay):
		self.frames.append(frame)
		self.delays.append(delay)

	def getCurrentFrame(self, timeScale):
		if len(self.frames) == 1:
			return self.frames[0]

		self.time += timeScale
		while self.time > self.delays[self.currentFrameIndex]:
			self.time -= self.delays[self.currentFrameIndex]
			self.currentFrameIndex += 1
			if self.currentFrameIndex >= len(self.frames):
				self.currentFrameIndex = 0

		returnFrame = self.frames[self.currentFrameIndex]
		return self.frames[self.currentFrameIndex]

	def reset(self):
		self.currentFrameIndex = 0
		self.time = 0
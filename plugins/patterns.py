__authors__ = ['Stew Francis']

import csv
import DDRPi
import time

from DDRPi import DDRPiPlugin

class Filter(object):
	
	def process(self, frame):
		raise NotImplementedError
	
class PatternFilter(Filter):
	
	def __init__(self, patternFile, beatService):
		self.frameIndex = 0
		self.frameTime = 0
		self.beatService = beatService
		
		with open(patternFile) as csvFile:
			reader = csv.reader(csvFile)
			patternMeta = reader.next()
			height = int(patternMeta[1])
			framesPerBeat = int(patternMeta[2])
			
			rows = list()
			
			for row in reader:
				rows.append([DDRPi.hexToTuple(colour) for colour in row])
				
		self.frames = [rows[i * height : (i+1) * height] for i in range(0, len(rows) / height)]
		print framesPerBeat
		self.beatsPerFrame = 1 / float(framesPerBeat)
		print "beats per frame: %s" % self.beatsPerFrame
	
	def process(self, frame):
		return self.frames[self.__getFrameIndex()]
		
	def __getFrameIndex(self):
		#calculate whether or not we need to advance the frame index
		tim = time.time()
		if tim > self.frameTime:
			# calculate the time of the next frame
			self.frameTime = self.beatService.getTimeOfNextBeatInterval(self.beatsPerFrame)
			
			toReturn = self.frameIndex
			#calculate next frame index
			self.frameIndex = (self.frameIndex + 1) % len(self.frames)
			return toReturn
		else:
			return self.frameIndex
		
class ColourMorphFilter(Filter):
	
	def __init__(self, beatService):
		self.beatService = beatService
	
	def process(self, frame):
		# magic beat beans: 1/(e^x^2)
		# 1/e^(20x^2) seems good between -1 and +1
		pass
		
		
class BeatService(object):
	
	def __init__(self):
		self.beatLength = 0.5
		self.lastBeatTime = time.time()
	
	def getTimeOfNextBeatInterval(self, beatInterval):
		intervalLength = self.beatLength * beatInterval
		tim = time.time()
		
		# calculate the next beat interval of beatInterval
		intervalTime = self.__getLastBeatTime(tim)
		while intervalTime < tim:
			intervalTime += intervalLength
		return intervalTime
		
	def __getLastBeatTime(self, tim):
		while self.lastBeatTime + self.beatLength < tim:
			self.lastBeatTime += self.beatLength
		return self.lastBeatTime
		

class Patterns(DDRPiPlugin):

	def configure(self, config, image_surface):
		self.surface = image_surface
		self.filters = list()
		self.beatService = BeatService()
		self.filters.append(PatternFilter("frames.csv", self.beatService))
	
	def display_preview(self):
		pass

	def start(self):
		pass

	def stop(self):
		pass

	def handle(self, event):
		pass

	def update_surface(self):
		frame = reduce(lambda x, y: y.process(x), self.filters, list())
		
		for x in range(0, self.surface.width):
			row = frame[x]
			for y in range(0, self.surface.height):
				self.surface.draw_tuple_pixel(x, y, row[y])
		
		self.surface.blit()

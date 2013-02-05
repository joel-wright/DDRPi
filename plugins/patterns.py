__authors__ = ['Stew Francis']

import csv
import DDRPi
import time
import math
import colorsys

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
				#convert to float representation
				rows.append([hexToFloatTuple(colour) for colour in row])
				
		self.frames = [rows[i * height : (i+1) * height] for i in range(0, len(rows) / height)]
		self.beatsPerFrame = 1 / float(framesPerBeat)
	
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

def hexToFloatTuple(hexString):
	(r, g, b) = DDRPi.hexToTuple(hexString)
	return (r/float(255), float(g/255), float(b/255))

class ColourFilter(Filter):
	
	def __init__(self, rgb):
		self.rgb = rgb
		
	def process(self, frame):
		#for each cell, apply the hue adjustment
		return [[tuple([c1*c2 for c1,c2 in zip(self.rgb, rgb)]) for rgb in row] for row in frame]
		
		
class BeatHueAdjustmentFilter(Filter):
	
	def __init__(self, beatService, hueAdjustment):
		self.beatService = beatService
		self.hueAdjustment = hueAdjustment
	
	def process(self, frame):		
		# beat position 0 -> 1, adjust to vary from function varies from -1 ->
		# 0-0.5 -> 0-1
		# 0.5-1 -> -1-0
		x = self.beatService.getBeatPosition()
		if x < 0.5:
			x *= 2
		else:
			x = 2 * (x - 1)
		
		#calculate how much we need to add to the hue, based on beat position
		frameHueAdjustment = self.hueAdjustment / (math.e ** ((5*x) ** 2))
		
		#for each cell, apply the hue adjustment
		return [[self.__adjustHue(frameHueAdjustment, rgb) for rgb in row] for row in frame]
	
	def __adjustHue(self, adjustment, rgb):
		(r, g, b) = rgb
		(h, l, s) = colorsys.rgb_to_hls(r, g, b);
		# inc and wrap h
		h = ((h + adjustment) % 1 + 1 % 1)
		return colorsys.hls_to_rgb(h, l, s)
		
		
class BeatService(object):
	
	def __init__(self):
		self.beatLength = 0.75
		self.lastBeatTime = time.time()
	
	def getTimeOfNextBeatInterval(self, beatInterval):
		intervalLength = self.beatLength * beatInterval
		tim = time.time()
		
		# calculate the next beat interval of beatInterval
		intervalTime = self.__getLastBeatTime(tim)
		while intervalTime < tim:
			intervalTime += intervalLength
		return intervalTime
	
	def getBeatPosition(self):
		tim = time.time()
		return (tim - self.__getLastBeatTime(tim)) / self.beatLength
		
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
		self.filters.append(ColourFilter((1.0, 0.0, 1.0)))
		self.filters.append(BeatHueAdjustmentFilter(self.beatService, 0.2))
	
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
				self.surface.draw_float_tuple_pixel(x, y, row[y])
		
		self.surface.blit()

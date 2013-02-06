__authors__ = ['Stew Francis']

import csv
import time
import math
import colorsys

from DDRPi import DDRPiPlugin
from lib.utils import ColourUtils

class Filter(object):
	
	def process(self, frame):
		raise NotImplementedError
	
class PatternFilter(Filter):
	
	def __init__(self, patternFile, beatService):
		self.frameIndex = 0
		self.frameTime = 0
		self.__beatService = beatService
		
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
			self.frameTime = self.__beatService.getTimeOfNextBeatInterval(self.beatsPerFrame)
			
			toReturn = self.frameIndex
			#calculate next frame index
			self.frameIndex = (self.frameIndex + 1) % len(self.frames)
			return toReturn
		else:
			return self.frameIndex

def hexToFloatTuple(hexString):
	(r, g, b) = ColourUtils.hexToTuple(hexString)
	rf = r/float(255)
	gf = g/float(255)
	bf = b/float(255);
	return (rf, gf, bf)

class MotionBlurFilter(Filter):
	
	def __init__(self, decayFactor):
		self.__decayFactor = decayFactor;
		self.__previous = None
		
	def process(self, frame):
		self.__previous = self.__decay(self.__previous)
		self.__previous = self.__overlay(frame, self.__previous)
		return self.__previous
	
	def __decay(self, frame):
		if self.__previous == None: return None
		return [[MotionBlurFilter.__applyDecay(self.__decayFactor, rgb) for rgb in row] for row in frame]
	
	def __overlay(self, topFrame, bottomFrame):
		if bottomFrame == None: return topFrame
		frameOfPairedRows = zip(topFrame, bottomFrame)
		return [[self.__blend(pair[0], pair[1]) for pair in zip(rowPairs[0], rowPairs[1])] for rowPairs in frameOfPairedRows]

	@staticmethod
	def __blend(rgb1, rgb2):
		return (max(rgb1[0], rgb2[0]), max(rgb1[1], rgb2[1]), max(rgb1[2], rgb2[2]))
	
	@staticmethod
	def __applyDecay(decayFactor, rgb):
		(r, g, b) = rgb
		(h, l, s) = colorsys.rgb_to_hls(r, g, b);
		l *= decayFactor
		return colorsys.hls_to_rgb(h, l, s)

class ColourFilter(Filter):
	
	def __init__(self, rgb):
		self.rgb = rgb
		
	def process(self, frame):
		#for each cell, apply the rgb filter
		return [[(self.rgb[0] * rgb[0], self.rgb[1] * rgb[1], self.rgb[2] * rgb[2]) for rgb in row] for row in frame]
		
		
class BeatHueAdjustmentFilter(Filter):
	
	def __init__(self, beatService, hueAdjustment):
		self.__beatService = beatService
		self.hueAdjustment = hueAdjustment
	
	def process(self, frame):		
		# beat position 0 -> 1, adjust to vary from function varies from -1 ->
		# 0-0.5 -> 0-1
		# 0.5-1 -> -1-0
		x = self.__beatService.getBeatPosition()
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
		self.__surface = image_surface
		self.__beatService = BeatService()
		self.__patternIndex = -1
		self.__nextPatternTime = 0
		self.__patternDisplaySecs = 30
		
		self.__patterns = [
			[
				PatternFilter("plugins/nyan.csv", self.__beatService)
			],
			[
				PatternFilter("plugins/line.csv", self.__beatService),
				MotionBlurFilter(0.9),
				ColourFilter((1.0, 0.0, 1.0)),
				BeatHueAdjustmentFilter(self.__beatService, 0.2)
			]
		]
	
	def display_preview(self):
		pass

	def start(self):
		pass

	def stop(self):
		pass

	def handle(self, event):
		pass

	def update_surface(self):
		frame = self.__apply(self.__getActivePattern())
		
		for y in range(0, self.__surface.height):
			row = frame[y]
			for x in range(0, self.__surface.width):
				self.__surface.draw_float_tuple_pixel(x, y, row[x])
		
		self.__surface.blit()
		
	def __apply(self, filters):
		return reduce(lambda x, y: y.process(x), filters, list())
	
	def __getActivePattern(self):
		tim = time.time()
		if self.__nextPatternTime < tim:
			self.__patternIndex = (self.__patternIndex + 1) % len(self.__patterns)
			self.__nextPatternTime = tim + self.__patternDisplaySecs
		
		return self.__patterns[self.__patternIndex]
		

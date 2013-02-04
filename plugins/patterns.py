__authors__ = ['Stew Francis']

import csv
import DDRPi

from DDRPi import DDRPiPlugin

class Filter(object):
	
	def process(self, input):
		raise NotImplementedError
	
class PatternFilter(Filter):
	
	def configure(self):
		self.frameIndex = 0
		self.beatLength = 0
		# framelength = beatLength x beatsPerFrame
		# if after time of next frame, calculate time for next frame, and update frame
		# ask beat service for time of next beat, and calculate time of next frame
		self.frameLength = beatLength x 
		
		with open("plugins/frames.csv") as csvFile:
			reader = csv.reader(csvFile)
			patternMeta = reader.next()
			width = int(patternMeta[0])
			height = int(patternMeta[1])
			beatsPerFrame = int(patternMeta[3])
			
			rows = list()
			
			for row in reader:
				rows.append([DDRPi.hexToTuple(colour) for colour in row])
				
		self.frames = [rows[i * height : (i+1) * height] for i in range(0, len(rows) / height)]
	
	def process(self, input):
		return self.frames[__getFrameIndex()]
		
	def __getFrameIndex(self):
		#calculate whether or not we need to advance the frame index
		time = time()
		if _requiresNewFrame():
			toReturn = self.frameIndex
			self.frameIndex = (self.frameIndex + 1) % len(self.frames)
			self.timeOfLastBeat = time
			return toReturn
		else:
			return self.frameIndex
		
	def __requiresNewFrame(self):
		# calculate whether or not we have advanced a beat
		time - self.timeOfLastBeat > self.beatLength			

class Patterns(DDRPiPlugin):

	def configure(self, config, image_surface):
		self.surface = image_surface
		self.filters = list()
		filter = PatternFilter()
		filter.configure()
		self.filters.append(filter)
	
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
		
	def get_frame():
		pass

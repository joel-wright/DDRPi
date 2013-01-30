__authors__ = ['Joel Wright']

import random
import time

from DDRPi import DDRPiPlugin

class SimplePlugin(DDRPiPlugin):
	def configure(self, config, image_surface):
		"""
		This is an example of an end user module - need to make sure we can get
		the main image surface and config to write to them both...
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface

	def __name__(self):
		return 'Simple Plugin'

	def start(self):
		"""
		Start writing to the surface
		"""
		# Setup recurring events
		return None

	def stop(self):
		"""
		Stop writing to the surface and clean up
		"""
		# Stop recurring events
		return None
		
	def handle(self, event):
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""
		return None
		
	def update_surface(self):
		"""
		Write the updated plugin state to the dance surface and blit
		"""
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		
		for x in range(0,w):
			for y in range(0,h):
				r = random.randint(0,255)
				g = random.randint(0,255)
				b = random.randint(0,255)
				c = self.ddrpi_surface.tupleToHex((r,g,b))
				self.ddrpi_surface.draw_pixel(x,y,c)

		time.sleep(0.05)
		self.ddrpi_surface.blit()

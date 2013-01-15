__authors__ = ['Joel Wright']

from DDRPi import DDRPiPlugin

class SimplePlugin(DDRPiPlugin):
	def config(self, config, image_surface):
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

	def stop(self):
		"""
		Stop writing to the surface and clean up
		"""

	def modify(self):
		"""
		We'll probably need a timer event for the plugin so that we can animate
		the updates.
		"""
		# TODO: A simple animated display

	def draw(self):
		"""
		Draw the internal representation onto the floor so we can start again
		"""

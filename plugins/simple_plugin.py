__authors__ = ['Joel Wright']

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

	def stop(self):
		"""
		Stop writing to the surface and clean up
		"""
		# Stop recurring events
		
	def handle(self, event)
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""
		
	def update_surface(self):
		"""
		Write the updated plugin state to the dance surface and blit
		"""

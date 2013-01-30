__authors__ = ['Joel Wright','Mark McArdle']

class DDRPiPlugin(object):
	def configure(self):
		"""
		Called to configure the plugin before we start it.
		"""
		raise NotImplementedError

	def start(self):
		"""
		Start the plugin.
		"""
		raise NotImplementedError

	def stop(self):
		"""
		Stop the plugin if necessary - e.g. stop writing to the dance surface.
		"""
		raise NotImplementedError
		
	def handle(self, event):
		"""
		Handle any pygame events sent to the plugin from the main loop
		"""
		raise NotImplementedError
		
	def update_surface(self):
		"""
		Write the updated plugin state to the dance surface and blit
		"""
		raise NotImplementedError
		

class PluginRegistry(object):
	def __init__(self):
		self.__registry__ = {}

	def register(self, name, item):
		self.__registry__[name] = item

	def get_names(self):
		return self.__registry__.keys()
		
	def get_plugin(self, name):
		return self.__registry__[name]

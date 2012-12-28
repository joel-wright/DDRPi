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
		

class PluginRegistry(object):
	def __init__(self):
		self.__registry__ = {}

	def register(self, name, item):
		self.__registry__[name] = item

	def values(self):
		return self.__registry__.values()

	def items(self):
		return self.__registry__.items()

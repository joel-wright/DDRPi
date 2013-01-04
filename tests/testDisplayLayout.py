__authors__ = ['Joel Wright']

from layout import DisplayLayout

class testDisplayLayout(object):
	def __init__(self, config):
		self.config = config
	
	def simpleTest(self):
		layout = DisplayLayout(self.config)

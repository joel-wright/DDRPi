__authors__ = ["Joel Wright"]

from plugins_test import registry
from plugins_base import TestPlugin

class TestPlugin2(TestPlugin):
    name = "TestPlugin2"
    version = 0.01
    
    def __init__(self):
        self.initialised = True
    
    def config(self):
        self.configured = True

    def start(self):
        print("Started TestPlugin2")

    def stop(self):
        print("Stopped TestPlugin2")
                    
plugin = TestPlugin2()
registry.register(plugin.name, plugin)
                    

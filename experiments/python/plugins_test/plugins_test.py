__author__ = ['Joel Wright']

import os
import sys
import importlib
import registry
from plugins_base import TestPlugin

class TestMainPlugins(object):
    def __init__(self):
        self.plugins = {}
        self.__load_plugins()
        print("Registered Plugins %s" % registry.items())

    def __load_plugins(self):
        """
        Load the plugins from the config plugin directory
        """
        print("Loading plugins from plugin directory")
        plugins_found = self.__find_plugins("plugins")
        print("Plugins found: %s" % self.plugins)
        
    def __find_plugins(self, plugin_folder):
        """
        Find the loadable plugins in the given plugin folder.
        
        Returns:
            A list of plugins that can be loaded.
        """
        print("Searching for plugins in %s" % plugin_folder)
        plugins = []
        
        for root, dirs, files in os.walk(plugin_folder):
            for fname in files:
                if fname.endswith(".py") and not fname.startswith("__"):
                    fpath = os.path.join(root, fname)
                    mname = fpath.rsplit('.', 1)[0].replace('/', '.')
                    importlib.import_module(mname)
            
            for plugin in TestPlugin.__subclasses__():
                print("name: %s" % plugin.__name__)
                self.plugins[plugin.__name__] = plugin


# Start the test
if __name__ == "__main__":
	test = TestMainPlugins()

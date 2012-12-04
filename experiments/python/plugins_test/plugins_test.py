__author__ = ['Joel Wright']

import logging
import os
import sys
import importlib

class TestPlugin(object):
    def configure(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class TestMainPlugins(object):
    def __init__(self):
        self.plugins = {}
        self.__load_plugins()

    def __load_plugins(self):
        """
        Load the plugins from the config plugin directory
        """
        logging.info("Loading plugins from plugin directory")
        plugins_found = self.__find_plugins("plugins")
        print("Plugins found: %s" % self.plugins)
        
    def __find_plugins(self, plugin_folder):
        """
        Find the loadable plugins in the given plugin folder.
        
        Returns:
            A list of plugins that can be loaded.
        """
        logging.info("Searching for plugins in %s" % plugin_folder)
        plugins = []
        
        for root, dirs, files in os.walk(plugin_folder):
            for fname in files:
                if fname.endswith(".py") and not fname.startswith("__"):
                    fpath = os.path.join(root, fname)
                    mname = fpath.rsplit('.', 1)[0].replace('/', '.')
                    sys.path.insert(0, plugin_folder)
                    module = importlib.import_module(mname)
                    for plugin in TestPlugin.__subclasses__():
                        print("name: %s" % plugin.__name__)
                        self.plugins[plugin.__name__] = plugin


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
                    
                    
# Start the test
if __name__ == "__main__":
	test = TestMainPlugins()

__author__ = ['Joel Wright']

import gtk
import cairo
import yaml
import pygtk
pygtk.require('2.0')

class Plugin(object):
    def configure(self):
        """
        Called to configure the plugin before we start it
        """
        raise NotImplementedError

    def start(self):
        """
        Start the plugin
        """
        raise NotImplementedError

    def stop(self):
        """
        Stop the plugin if necessary - e.g. stop writing to the dance surface
        """
        raise NotImplementedError


class DanceSurface(gtk.DrawingArea):
    """
    The class representing the drawable dance floor
    """
    def __init__(self, config):
        super(DanceSurface, self).__init__()

        self.config = config
        self.height = config["system"]["height"]
        self.width = config["system"]["width"]
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.height, self.width)

    def get_image_surface(self):
        return self.surface

    def expose(self, widget, event):
        """
        Deal with an expose event and draw the image surface

        Do we draw to the RPi USB here?
        """


class DDRPi(gtk.Window):
    """
    The Main class - should load plugins and manage access to the DanceSurface object
    """
    def __init__(self):
        """
        Initialise the dance floor
        """
        super(DDRPi, self).__init__()

        self.config = self.__load_config()
        self.dance_surface = DanceSurface(self.config)
        self.plugins = []

    def __load_config(self):
        f = open('config.yaml')
        data = yaml.load(f)
        f.close()
        return data

    def __load_plugins(self):
        """
        Load the plugins from the config plugin directory
        """
        plugin_folder = self.config["system"]["plugin_dir"]


# Start the dance floor application
if __name__ == "__main__":
	dance_floor = DDRPi()
	gtk.main()

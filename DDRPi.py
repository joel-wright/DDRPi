__author__ = 'Joel Wright'

import gtk
import cairo
import yaml

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

    def __load_config(self):
        f = open('config.yaml')
        data = yaml.load(f)
        f.close()
        return data




DDRPi()
gtk.main()
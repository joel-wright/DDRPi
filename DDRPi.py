__author__ = 'Joel Wright'

import gtk
import cairo
import yaml

class DanceSurface(gtk.DrawingArea):
    """
    The class representing the drawable dance floor
    """
    def __init__(self):
        super(DanceSurface, self).__init__()

        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 300, 300)

class DDRPi(gtk.Window):
    """
    The Main class - should load plugins and manage access to the DanceSurface object
    """
    def __init__(self):
        """
        Initialise the dance floor
        """
        super(DDRPi, self).__init__()

        self.dance_surface = DanceSurface()
        self.config = self.__load_config()

    def __load_config():
        f = open('config.yaml')
        data = yaml.load(f)
        f.close()
        return data

DDRPi()
gtk.main()
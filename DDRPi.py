__author__ = ['Joel Wright']

import gtk
import cairo
import yaml
import pygtk
import logging
pygtk.require('2.0')
from layout import DisplayLayout
from plugins_base import DDRPiPlugin, PluginRegistry

class DanceSurface(gtk.DrawingArea):
    """
    The class representing the drawable dance floor. This is a wrapper around
    a Cairo ImageSurface, so that we can pass the ImageSurface to the display
    plugins, and react to any changes made by updating the display and sending
    the appropriate updates to the dance floor through the serial port.
    """
    def __init__(self, width, height):
        super(DanceSurface, self).__init__()

        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.height, self.width)

    def get_image_surface(self):
        return self.surface

    def expose(self, widget, event):
        """
        Deal with an expose event and draw the image surface

        Do we draw to the RPi USB here?
        """
        # TODO: Draw to the widget and output to the serial port


class DDRPi(gtk.Window):
    """
    The Main class - should load plugins and manage access to the DanceSurface object
    """
    def __init__(self):
        """
        Initialise the DDRPi Controller app.
        """
        super(DDRPi, self).__init__()

        # GTK setup stuff
        self.set_title("DDRPi Controller")
        self.set_size_request(800,600)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        
        # TODO: Load the Glade layout

        # Load the application config
        self.config = self.__load_config()
        
        # Set up plugin registry
        self.__registry__ = PluginRegistry()
        self.__register_plugins(self.config["system"]["plugin_dir"])
        
        # Create the layout widget and calculate floor size
        self.layout = DisplayLayout(self.config["modules"])
        (x,y) = self.layout.calculate_floor_size()
        self.layout.connect("layout-changed", self.changed_layout)
        
        # Create the dance floor widget
        self.dance_surface = DanceSurface(x, y)
        self.plugins = []

    def __load_config(self):
        """
        Load the config file into a dictionary.
        
        Returns:
            The dictionary resulting from loading the YAML config file.
        """
        f = open('config.yaml')
        data = yaml.load(f)
        f.close()
        return data
        
    def __register_plugins(self, plugin_folder):
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
            
            for plugin in DDRPiPlugin.__subclasses__():
                print("name: %s" % plugin.__name__)
                pinst = plugin()
                self.__registry__.register(pinst.__name__, pinst)
        
    def changed_layout(self, widget):
        """
        Called on layout change to dedefine the DanceFloor size/shape
        """
        # Get the new size and shape
        (x,y) = self.layout.calculate_floor_size()
        
        # Create a new dance surface
        self.dance_surface = DanceSurface(x, y)
        
        # TODO: Reconfigure the running plugin (or reload the running plugin)
        #       Need to create a layout changed event - see URL below for details:
        #       http://zetcode.com/gui/pygtk/signals/


# Start the dance floor application
if __name__ == "__main__":
	dance_floor = DDRPi()
	gtk.main()

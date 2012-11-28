__authors__ = ['Joel Wright']

import gtk
from DDRPi import Plugin

class DisplayLayout(gtk.DrawingArea):
    def __init__(self):
        super(DisplayLayout, self).__init__()

    def load_config(self, config):
        self.tile_config = config

    def expose(self):
        draw_modules()
        
    def draw_modules(self):
        """
        Draw the modules layout onto the drawing area 
        """
        (size_x, size_y) = calculate_floor_size()
        
    def calculate_floor_size(self):
        x_extent, y_extent = 0
        
        for module in self.config:
            module_data = self.config[module]
            module_orientation = module_data["orientation"]
            module_height = module_data["height"]
            module_width = module_data["width"]
            
            max_x, max_y = {
                'N': (module_width + module_data["x_position"], module_height + module_data["y_position"]),
                'E': (module_height + module_data["x_position"], module_width + module_data["y_position"]),
                'S': (module_width + module_data["x_position"], module_height + module_data["y_position"]),
                'W': (module_height + module_data["x_position"], module_width + module_data["y_position"]),
            }[module_orientation]
            
            if (max_x > x_extent):
                x_extent = max_x
            if (max_y > y_extent):
                y_extent = max_y
                
        return (x_extent, y_extent)
        
        
        
        



__authors__ = ['Joel Wright']

from DDRPi import Plugin

class DisplayLayout(object):
    def __init__(self, config):
        super(DisplayLayout, self).__init__()
        load_config(config)

    def load_config(self, config):
        self.tile_config = config

    def expose(self):
        """
        Whenever the widget is exposed, draw the module layout to the display.
        """
        draw_modules()
        
    def draw_modules(self):
        """
        Draw the modules layout onto the drawing area. This method draws the
        described layout onto the display, labelling the pixels with their
        dance floor address.
        """
        (size_x, size_y) = calculate_floor_size()
        
        # TODO: Draw the layout onto the widget
        
    def calculate_floor_size(self):
        """
        Calculate the total size in pixels described by the config file. Note
        that we do not guarantee that all pixels will be used, this simply
        returns the max x and y coordinates described.
        
        We will deal with overlapping boards and gaps later.
        
        Returns:
            A pair containing the maximum x and y coordinated required by the
            dance floor
        """
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
                
        



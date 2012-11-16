__author__ = 'Joel Wright'

class DisplayLayout(gtk.Window):
    def __init__(self, config, image_surface):
        super(DisplayLayout, self).__init__()

        # This is an example of an end user module - need to make sure we can get the main image surface and config
        # to write to them both...
        self.ddrpi_config = config
        self.ddrpi_surface = image_surface



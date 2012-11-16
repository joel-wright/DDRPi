__author__ = 'Joel Wright'

class DanceSurface(gtk.Window):
    def __init__(self):
        super(DanceSurface, self).__init__()

        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 300, 300)

class DDRPi(gtk.Window):
    def __init__(self):
        super(DDRPi, self).__init__()

        self.dance_surface = DanceSurface()



gtk.main()
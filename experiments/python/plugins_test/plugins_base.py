__authors__ = ["Joel Wright"]

class TestPlugin(object):
    def configure(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


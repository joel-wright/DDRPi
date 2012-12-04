
__registry__ = {}

def register(name, item):
    __registry__[name] = item

def values():
    return __registry__.values()

def items():
    return __registry__.items()

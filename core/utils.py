from manim import *
class Props:
    def __init__(self, namespace, toRegister):
        for k,v in namespace.items():
            if k in toRegister:
                self.__dict__[k] = v

class Namespace:
    def __init__(self, default, kwargs):
        to_pop = []  # consume the kwargs we use
        for k,v in default.items():
            if k in kwargs:
                self.__dict__[k] = kwargs[k]
                to_pop += [k]
            else:
                self.__dict__[k] = v
        for k in to_pop:
            kwargs.pop(k)

class ABWComponent:
    def __init__(self, mobs, props, kwargs):
        self.mobs  = Namespace(mobs, kwargs)
        self.props = Namespace(props, kwargs)
        self.mob = VGroup()
        self.mob.add(*mobs.values())
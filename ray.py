from vec3 import Vec

class Ray:
    def __init__(self, origin=Vec(0,0,0), direction=Vec(0,0,0)):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + t*self.direction


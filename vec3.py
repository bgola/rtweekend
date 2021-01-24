import math
from random import random

class Vec(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def r(self):
        return self.x
    
    @property
    def g(self):
        return self.y

    @property
    def b(self):
        return self.z  

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def random(mi=0, ma=1):
        return Vec(mi+random()*ma, mi+random()*ma, mi+random()*ma)

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec.random(-1,1)
            if(p.length_squared() >= 1): continue
            return p

    @staticmethod
    def random_unit_vector():
        return Vec.random_in_unit_sphere().unit_vector()

    @staticmethod
    def random_in_hemisphere(normal):
        in_unit_sphere = Vec.random_in_unit_sphere()
        if Vec.dot(in_unit_sphere, normal) > 0:
            return in_unit_sphere
        return -in_unit_sphere

    @staticmethod
    def cross(v1, v2):
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.x * v2.x - v1.x * v2.z
        z = v1.z * v2.y - v1.y * v2.x
        return Vec(x, y, z)

    @staticmethod
    def normalize(v):
        return v / v.norm()

    def reflect(self, n):
        return self - 2*Vec.dot(self,n)*n

    def near_zero(self):
        s = 1e-8
        return (abs(self.x) < s) and (abs(self.y) < s) and (abs(self.z) < s)

    def norm(self):
        return math.sqrt(Vec.dot(self, self))

    def unit_vector(self):
        return self / self.length()

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y, self.z + v.z)

    def __neg__(self):
        return Vec(-self.x, -self.y, -self.z)

    def __sub__(self, v):
        return self + (-v)

    def __mul__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            return Vec(self.x * v, self.y * v, self.z * v)

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    def __rmul__(self, v):
        return self.__mul__(v)

    def __truediv__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y, self.z / v.z)
        else:
            return Vec(self.x / v, self.y / v, self.z / v)

    def __str__(self):
        return '[ %.4f, %.4f, %.4f ]' % (self.x, self.y, self.z)

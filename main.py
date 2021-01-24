import sys
from random import random
import math
from math import pi

from vec3 import Vec
from ray import Ray
from mat import *

Color = Vec
Point3 = Vec

inf = float('inf')

def rand(mi,ma):
    return mi + random()*ma

def clamp(x, mi, ma):
    return max(mi, min(x, ma))

def degrees_to_radians(degrees):
    return degrees * pi / 180.0

class Camera:
    def __init__(self, aspect_ratio=16/9, origin=Vec(0,0,0), viewport_height=2, focal_length=1.0):
        self.aspect_ratio = aspect_ratio
        self.viewport_height = viewport_height
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0
        self.origin = Vec(0,0,0)
        self.horizontal = Vec(self.viewport_width, 0, 0)
        self.vertical = Vec(0, self.viewport_height, 0)
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - Vec(0, 0, self.focal_length)

    def get_ray(self, u , v):
        return Ray(self.origin, self.lower_left_corner + u*self.horizontal + v*self.vertical - self.origin)

class HitRecord:
    def __init__(self, p=0, normal=0, t=0, front_face = False):
        self.p = p
        self.normal = normal
        self.t = t
        self.material = None
        self.front_face = front_face

    def set_face_normal(self, r, outward_normal):
        self.front_face = Vec.dot(r.direction, outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal

class Hittable:
    def hit(self, r, t_min, t_max, rec):
        pass

class Sphere(Hittable):
    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = radius
        self.material = mat

    def hit(self, r, t_min, t_max, rec):
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = Vec.dot(oc, r.direction)
        c = oc.length_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c
        if (discriminant < 0):
            return False
        sqrtd = math.sqrt(discriminant)

        # find the nearest root that lies in the acceptable range
        root = (-half_b - sqrtd) / a
        if (root < t_min or t_max < root): 
            root = (-half_b + sqrtd) / a
            if (root < t_min or t_max < root): 
                return False
        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material
        return True


class World(Hittable):
    def __init__(self):
        self.objs = []

    def add(self, obj):
        self.objs.append(obj)

    def hit(self, r, t_min, t_max, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max
        for obj in self.objs:
            if obj.hit(r, t_min, closest_so_far, temp_rec):
                    hit_anything = True
                    closest_so_far = temp_rec.t
                    rec.t = temp_rec.t
                    rec.p = temp_rec.p
                    rec.normal = temp_rec.normal
                    rec.front_face = temp_rec.front_face
                    rec.material = temp_rec.material
        return hit_anything


def write_color(f, color, samples_per_pixel):
    scale = 1/samples_per_pixel
    r,g,b = [ clamp(math.sqrt(x*scale), 0, 0.999) for x in  [color.r, color.g, color.b] ]
    f.write(f"{int(r*256)} {int(g*256)} {int(b*256)}\n")

world = World()
for x in range(130):
        world.add(Sphere(Vec(random()*20-10, random()*20-10, random()*-20), random(), 
                Metal(Color(random(),random(),random()))))

#world.add(Sphere(Point3(0,0,-1), 0.5, Metal(Color(1,0.3,0.8))))
#world.add(Sphere(Point3(0,-100.5, -1), 100, Metal(Color(0.2,1,0.5))))

def ray_color(r, world, depth):
    rec = HitRecord()
    if (depth<=0):
        return Color(0,0,0)

    if world.hit(r, 0.001, inf, rec):
        scattered = Ray()
        attenuation = Color()
        if rec.material.scatter(r, rec, attenuation, scattered):
            return  attenuation * ray_color(scattered, world, depth-1)
            # experimenting with black and white
            #c = (color.x + color.y + color.z)/3
            #return Color(c,c,c)

        return Color(0,0,0)
    ud = r.direction.unit_vector()
    t = 0.5 * (ud.y + 1)
    return (1-t) * Vec(1,1,1) + t*Vec(0.5,0.7,1.0)
    # return (1-t) * Vec(1,1,1) + t*Vec(0.0,0.0,0.0)

aspect_ratio = 16/9

w = 1500
h = int(w/aspect_ratio)
samples_per_pixel = 20

camera = Camera(aspect_ratio)
max_depth = 30

f=sys.stdout;
e=sys.stderr;
f.write("P3\n")
f.write(f"{w} {h}\n255\n")
for j in range(h-1,-1,-1):
    e.write(f"\rRemaining: {j} ")
    e.flush
    for i in range(w):
        c = Color(0,0,0)
        for s in range(samples_per_pixel):
            u = (i + random()) / (w-1)
            v = (j + random()) / (h-1)
            c += ray_color(camera.get_ray(u,v), world, max_depth)
        write_color(f, c, samples_per_pixel)

f.close()
e.write("\nDone\n")

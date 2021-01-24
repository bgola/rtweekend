from vec3 import Vec
from ray import Ray


class Material:
    def scatter(r_in, rec, attenuation, scattered):
        pass

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + Vec.random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        scattered.origin = rec.p
        scattered.direction = scatter_direction
        attenuation.x = self.albedo.r
        attenuation.y = self.albedo.g
        attenuation.z = self.albedo.b
        return True

class Metal:
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = r_in.direction.unit_vector().reflect(rec.normal)
        scattered.origin = rec.p
        scattered.direction = reflected
        attenuation.x = self.albedo.r
        attenuation.y = self.albedo.g
        attenuation.z = self.albedo.b
        return (Vec.dot(scattered.direction, rec.normal) > 0)

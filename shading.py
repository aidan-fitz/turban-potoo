from linalg import *


class Light:
    channels = ['r', 'g', 'b']
    refl_types = ['ambient', 'diffuse', 'specular']

    def __init__(self):
        self.constants = {
            ('ambient', 'r'): 0.0,
            ('ambient', 'g'): 0.0,
            ('ambient', 'b'): 0.0,
            ('diffuse', 'r'): 0.0,
            ('diffuse', 'g'): 0.0,
            ('diffuse', 'b'): 0.0,
            ('specular', 'r'): 0.0,
            ('specular', 'g'): 0.0,
            ('specular', 'b'): 0.0,
        }
        self.lights = {}

    def get_constants(self):
        return self.constants

    def get_constant(self, refl_type, color):
        return self.constants[refl_type, color]

    def set_constant(self, refl_type, color, value):
        self.constants[refl_type, color] = value

    def normalize_constants(self):
        for color in channels:
            S = sum(map(lambda refl: self.get_constant(refl, color), refl_types))
            if S:
                for refl_type in refl_types:
                    self.constants[refl_type, color] /= S

    def add_light(self, point, color):
        if point is not None:
            self.lights[point] = color
        else:
            raise ValueError('Point cannot be None')

    def set_ambient_light(self, color):
        self.lights[None] = color

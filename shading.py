from draw import *

I_a = [40, 12, 35]
I_d = [200, 90, 60]
I_s = [0, 80, 40]

I = vector_sum(I_a, I_d, I_s)


class Light:
    channels = [RED, GREEN, BLUE]
    refl_types = ['ambient', 'diffuse', 'specular']

    FLAT = 0
    GOURAUD = 1
    PHONG = 2

    def __init__(self):
        self.constants = {
            'ambient': [0, 0, 0],
            'diffuse': [0, 0, 0],
            'specular': [0, 0, 0]
        }
        self.point_lights = []
        self.ambient_light = [0, 0, 0]

    def get_constants(self):
        return self.constants

    def get_constant(self, refl_type, color):
        return self.constants[refl_type][color]

    def set_constant(self, refl_type, color, value):
        self.constants[refl_type][color] = value

    def normalize_constants(self):
        for color in channels:
            S = sum(map(lambda refl: self.get_constant(refl, color), refl_types))
            if S > 1:
                for refl_type in refl_types:
                    self.constants[refl_type][color] /= S

    def add_light(self, point, color):
        self.point_lights.append( (point, color) )

    def get_ambient_light(self):
        return self.ambient_light

    def set_ambient_light(self, color):
        self.ambient_light = color

    def get_point_light(self, i):
        return self.point_lights[i]

    def set_point_light(self, i, point, color):
        self.point_lights[i] = (point, color)

    def remove_point_light(self, i):
        return self.point_lights.pop(i)

    def shade(self, matrix, index, mode):
        # Get ambient light
        I = self.ambient_light[:]
        for color in channels:
            # Multiply by ambient reflection constants
            I[color] *= self.get_constant('ambient', color)

            p = centroid(matrix, index)
            # Point lights
            for point, colour in self.point_lights:
                incident_vector = normalize(subtract(point, p))

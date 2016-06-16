from draw import *

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
        for color in Light.channels:
            # careful to use floats!!!
            S = float(sum(map(lambda refl: self.get_constant(refl, color), Light.refl_types)))
            #print color, 'sum = ', S
            if S > 1:
                for refl_type in Light.refl_types:
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

    def shade(self, matrix, index, mode=FLAT, view = [0, 0, 1]):
        # Get ambient light
        I = self.ambient_light[:]
        #print "ambient light:", I
        for color in Light.channels:
            # Multiply by ambient reflection constants
            I[color] *= self.get_constant('ambient', color)
            #print 'mult by ambient constant:', I

            p = centroid(matrix, index)
            # Point lights
            for point, colour in self.point_lights:
                incident_vector = normalize(subtract(point, p))
                normal = normalize(surface_normal(matrix, index))
                # Diffuse reflection
                cos_t = dot_product(incident_vector, normal)
                if cos_t > 0:
                    I[color] += colour[color] * self.get_constant('diffuse', color) * cos_t * cos_t
                #print '+ diffuse light:', I
                # Specular reflection
                #project incident_vector onto normal: shortcut
                reflect = subtract(mult(2*cos_t, normal), incident_vector)
                cos_a = dot_product(reflect, view)
                if cos_a > 0:
                    I[color] += colour[color] * self.get_constant('specular', color) * cos_a * cos_a
                #print '+ specular light:', I
        # cast back to integers
        return [int(v) for v in I]

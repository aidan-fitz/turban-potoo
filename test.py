from display import *
from draw import *
from shading import Light

screen = new_screen()

light = Light()
light.set_constant('ambient', RED, 1)
light.set_constant('ambient', GREEN, 1)
light.set_constant('ambient', BLUE, 1)
light.set_constant('diffuse', RED, 1)
light.set_constant('diffuse', GREEN, 1)
light.set_constant('diffuse', BLUE, 1)
light.set_constant('specular', RED, 1)
light.set_constant('specular', GREEN, 1)
light.set_constant('specular', BLUE, 1)
light.normalize_constants()

print 'light constants:', light.get_constants()

light.set_ambient_light([64, 64, 64])
light.add_light([-500, 500, 500], [255, 255, 255])


p1 = [100, 100, 100, 1]
p2 = [400, 100, 100, 1]
p3 = [400, 300, 100, 1]
#p4 = p1[:2] + [0, 1]
#p5 = p2[:2] + [0, 1]
#p6 = p3[:2] + [0, 1]

tri1 = [p1, p2, p3]
#tri2 = [p4, p5, p6]

#draw_triangle(tri2, 0, screen, [255, 0, 0], fill=True)
draw_polygons(tri1, screen, [0, 0, 255], light)

save_extension(screen, "test.ppm.gz")

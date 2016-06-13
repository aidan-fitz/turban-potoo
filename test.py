from display import *
from draw import *

screen = new_screen()

p1 = [100, 100, 100, 1]
p2 = [150, 100, 100, 1]
p3 = [150, 200, 100, 1]
p4 = p1[:2] + [0, 1]
p5 = p2[:2] + [0, 1]
p6 = p3[:2] + [0, 1]

tri1 = [p1, p2, p3]
tri2 = [p4, p5, p6]

draw_triangle(tri2, 0, screen, [255, 0, 0], fill=True)
draw_triangle(tri1, 0, screen, [0, 0, 255], fill=True)

save_ppm(screen, "test.ppm.gz")

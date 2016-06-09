from display import *
from draw import *
from draw3d import *

screen = new_screen()
triangle = [[100, 100, 270, 1], [450, 300, -60, 1], [150, 402, 100, 1]]
draw_triangle(triangle, 0, screen, [0, 255, 0], fill=True)
save_ppm(screen, "test.ppm")

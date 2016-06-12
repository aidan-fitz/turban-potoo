from display import *
from draw import *

screen = new_screen()
triangle = [[100, 100, 100, 1], [150, 100, 100, 1], [450, 200, 100, 1]]
draw_triangle(triangle, 0, screen, [0, 255, 0], fill=True)
save_ppm(screen, "test.ppm")

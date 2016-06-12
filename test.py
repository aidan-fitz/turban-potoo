from display import *
from draw import *

screen = new_screen()
p1 = [100, 100, 100, 1]
p2 = [150, 100, 105, 1]
p3 = [150, 200, 100, 1]
triangle = [p1, p2, p3]
draw_triangle(triangle, 0, screen, [0, 255, 0], fill=True)
save_ppm(screen, "test.ppm.gz")

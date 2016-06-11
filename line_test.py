from display import *
from draw import *

screen = new_screen()
# This line is in front and it's red
draw_line(screen, 50, 50, -14, 480, 390, 245, [255, 0, 0])
# This line is behind and it's blue
draw_line(screen, 100, 400, -20, 400, 1, -200, [0, 0, 255])

save_ppm(screen, "line_test.ppm")

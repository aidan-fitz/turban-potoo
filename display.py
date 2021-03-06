# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from os import remove


# CONSTANTS

XRES = 500
YRES = 500
MAX_COLOR = 255
DEFAULT_COLOR = [0, 0, 0, float("-Inf")]

# indices
RED     = 0
GREEN   = 1
BLUE    = 2
Z_INDEX = 3


# FUNCTIONS

def new_screen(width=XRES, height=YRES):
    screen = []
    for y in range(height):
        row = []
        screen.append(row)
        for x in range(width):
            screen[y].append(DEFAULT_COLOR[:])
    return screen

def plot(screen, color, x, y, z=666):
    #print x, y
    x = int(x)
    y = int(y)
    newy = YRES - 1 - y
    # z-buffering
    #print x, newy, screen[x][newy]
    if 0 <= x < XRES and 0 <= newy < YRES:
        #print x, y, z, screen[x][newy][Z_INDEX], color
        if z > screen[x][newy][Z_INDEX]:
            screen[x][newy] = color[:] + [z]

def clear_screen(screen):
    for y in range(len(screen)):
        for x in range(len(screen[y])):
            screen[x][y] = DEFAULT_COLOR[:]

def save_ppm(screen, fname):
    f = open(fname, 'w')
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range(len(screen)):
        row = ''
        for x in range(len(screen[y])):
            pixel = screen[x][y]
            row+= str(pixel[RED]) + ' '
            row+= str(pixel[GREEN]) + ' '
            row+= str(pixel[BLUE]) + ' '
        ppm+= row + '\n'
    f.write(ppm)
    f.close()

def save_extension(screen, fname):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm(screen, ppm_name)
    p = Popen(['convert', ppm_name, fname], stdin=PIPE, stdout=PIPE)
    p.communicate()
    # Keep the temp file for debugging
    remove(ppm_name)

def display(screen):
    ppm_name = 'pic.ppm'
    save_ppm(screen, ppm_name)
    Popen(['display', ppm_name], stdin=PIPE, stdout=PIPE)
    #remove(ppm_name)

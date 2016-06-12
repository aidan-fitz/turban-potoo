#!/usr/bin/python

from interpreter import run
import sys

if '--frame' in sys.argv:
    i = sys.argv.index('--frame')
    frame = int(sys.argv[i + 1])
    sys.argv.pop(i)
    sys.argv.pop(i)
else:
    frame = -1

if len(sys.argv) == 2:
    run(sys.argv[1], frame)
elif len(sys.argv) == 1:
    run(raw_input("please enter the filename of an mdl script file: \n"), frame)
else:
    print "Too many arguments."

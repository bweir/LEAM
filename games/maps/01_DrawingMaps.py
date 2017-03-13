#/usr/bin/env python

from lame import gfx     
from lame import map     
from lame import ctrl

def main():
    buf = gfx.start()
    map.start(buf)

    cave = map.load('gfx/cave.tmx')
    map.draw(cave, 0, 64)
    map.draw(cave, 0, 64, 0, 0, 128, 64)
    gfx.draw()
    ctrl.waitkey()

main()

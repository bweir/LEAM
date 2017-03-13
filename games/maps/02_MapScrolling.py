#/usr/bin/env python

from lame import gfx     
from lame import map     
from lame import ctrl    

def main():
    xoffset = 0
    yoffset = 0
    bound_x = 0
    bound_y = 0

    buf = gfx.start()
    map.start(buf)

    cave = map.load('gfx/cave.tmx')
    bound_x = map.width(cave) * 8 - gfx.SCREEN_W
    bound_y = map.height(cave) * 8 - gfx.SCREEN_H
    yoffset = bound_y

    while True:
        gfx.clear()
        ctrl.update()

        if ctrl.up():
            if yoffset > 0:
                yoffset -= 1
        if ctrl.down():
            if yoffset < bound_y:
                yoffset += 1
        if ctrl.left():
            if xoffset > 0:
                xoffset -= 1
        if ctrl.right():
            if xoffset < bound_x:
                xoffset += 1

        map.draw(cave, xoffset, yoffset)
        gfx.draw()

main()

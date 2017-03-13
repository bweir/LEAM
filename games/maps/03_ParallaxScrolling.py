#/usr/bin/env python

from lame import gfx     
from lame import map     
from lame import ctrl    

def main():
    xoffset = 0
    offsetw = 0
    w1 = 0
    dx = 0

    map.start(gfx.start())
    gfx.limit(gfx.FULLSPEED)
    cavelake = gfx.load('gfx/cavelake.png')
    cave = map.load('gfx/cave.tmx')
    cave2 = map.load('gfx/cave2.tmx')
    w1 = map.width(cave) * 8 - 128
    h1 = map.height(cave) * 8 - 64
    w2 = map.width(cave2) * 8 - 128
    h2 = map.height(cave2) * 8 - 64
    dx = w1 // w2
    dy = h1 // h2
    yoffset = 64

    while True:
        ctrl.update()
        if ctrl.left():
            if xoffset > 0:
                xoffset -= 2
        if ctrl.right():
            if xoffset < w1:
                xoffset += 2
        if ctrl.up():
            if yoffset > 0:
                yoffset -= 2
        if ctrl.down():
            if yoffset < h1:
                yoffset += 2
        gfx.blit(cavelake)
        gfx.invertcolor(True)
        map.draw(cave2, xoffset // dx, yoffset // dy)
        gfx.invertcolor(False)
        map.draw(cave, xoffset, yoffset)
        gfx.draw()

main()

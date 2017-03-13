import os
import sys

from lame import con
from lame import gfx 
from lame import log

import pytmx
from pytmx.util_pygame import load_pygame

composer = None

_maps = {}

def start(buf):
    global composer
    composer = buf

def load(filename):
    if filename in _maps:
        return _maps[filename]

    rootpath = os.path.abspath(con.SCRIPT)
    filepath = os.path.join(rootpath, filename)
    filepath = os.path.realpath(filepath)
    if not filepath.startswith(rootpath):
        log.error("Map not found: "+filename)
        sys.exit(1)

    log.info("Loading map "+filename)

    _maps[filename] = load_pygame(filename)
    return _maps[filename]

def draw(source,
         offset_x=0, offset_y=0,
         x1=0, y1=0,
         x2=gfx.SCREEN_W, y2=gfx.SCREEN_H):

    fx1 = (x1 + offset_x) // source.tilewidth
    fy1 = (y1 + offset_y) // source.tileheight
    fx2 = (x2 + offset_x) // source.tilewidth
    fy2 = (y2 + offset_y) // source.tileheight

    if fx2 % source.tilewidth > 0:
        fx2 += source.tilewidth
    if fy2 % source.tileheight > 0:
        fy2 += source.tileheight

    for y in range(fy1, fy2):
        for x in range(fx1, fx2):
            try:
                image = source.get_tile_image(x, y, 0)
                composer.blit(image, (x * source.tilewidth - offset_x,
                                      y * source.tileheight - offset_y))
            except TypeError:
                pass
            except ValueError:
                pass

def width(source):
    return source.width

def height(source):
    return source.height

#def TestPoint(x, y):
#    tilebase = 0
#    tilebase = 4 + word[map_levelmap][MX] * y + map_levelmap
#    if (byte[tilebase][x] & COLLIDEMASK):
#        return 1
#
#def TestCollision(objx, objy, objw, objh):
#    tilebase = 0
#    x = 0
#    y = 0
#    tx = 0
#    ty = 0
#    ty = word[map_tilemap][SY]
#    objh  = (word[map_levelmap][MY] * ty) <# (objh += objy)
#    objy #>= 0
#    if objh -= 1 <= objy:
#        return
#    tx = word[map_tilemap][SX]
#    objw  = (word[map_levelmap][MX] * tx) <# (objw += objx)
#    objx #>= 0
#    if objw -= 1 <= objx:
#        return
#    objx /= tx
#    objy /= ty
#    objw /= tx
#    objh /= ty
#    tilebase = 4 + word[map_levelmap][MX] * objy + map_levelmap
#    for y in range(objy, objh):
#        for x in range(objx, objw):
#            if (byte[tilebase][x] & COLLIDEMASK):
#                return (x+1)+((y+1) << 16)
#        tilebase += word[map_levelmap][MX]
#
#def TestMoveY(x, y, w, h, newy):
#    tmp = 0
#    ty = 0
#    if newy == y:
#        return
#    tmp = TestCollision(x, newy, w, h)
#    if not tmp:
#        return
#    ty  = word[map_tilemap][SY]
#    tmp = ((tmp >> 16)-1) * ty - newy
#    if newy > y:
#        return tmp - h
#    return tmp + ty
#
#def TestMoveX(x, y, w, h, newx):
#    tmp = 0
#    tx = 0
#    if newx == x:
#        return
#    tmp = TestCollision(newx, y, w, h)
#    if not tmp:
#        return
#    tx  = word[map_tilemap][SX]
#    tmp = ((tmp & int("0xFFFF",0))-1) * tx - newx
#    if newx > x:
#        return tmp - w
#    return tmp + tx
#

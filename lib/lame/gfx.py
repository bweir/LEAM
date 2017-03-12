from lame import log

import pygame
from pygame.locals import *

import sys

SCREEN_W = 128
SCREEN_H = 64
PIXEL_W = 4
PIXEL_H = 4

BLACK = (0,0,0)
WHITE = (255,255,255)
TRANSPARENT = (255,0,255)
GRAY = (128,128,128)

FULLSPEED = 40
HALFSPEED = 20
QUARTERSPEED = 10

composer = None
screen = None
inverted = False

clock = pygame.time.Clock()
speed = 0

def start(w=128, h=64, pw=4, ph=4, title=None):
    global composer
    global screen
    global PIXEL_W, PIXEL_H
    global SCREEN_W, SCREEN_H
    SCREEN_W = w
    SCREEN_H = h
    PIXEL_W = pw
    PIXEL_H = ph

    pygame.init()

    screen = pygame.display.set_mode(
            (SCREEN_W*PIXEL_W,
                SCREEN_H*PIXEL_H),
            pygame.DOUBLEBUF)

    composer = pygame.Surface((SCREEN_W, SCREEN_H))
    try:
        pygame.display.set_caption(title)
    except:
        pygame.display.set_caption(sys.argv[0])
    return composer

def draw():
    pygame.transform.scale(composer, 
            (SCREEN_W*PIXEL_W, 
                SCREEN_H*PIXEL_H),
            screen)

    if inverted:
        pixels = pygame.surfarray.pixels2d(screen)
        pixels ^= 2 ** 32 - 1
        del pixels

    pygame.display.flip()
    if speed > 0:
        clock.tick(speed)

def limit(frequency):
    global speed
    speed = frequency
    return

def invertscreen(enabled):
    global inverted
    inverted = enabled

def sync():
    return

_images = {}

def load(filename, width=None, height=None):

    if filename in _images:
        return _images[filename]

    log.info("Loading "+filename)

    d = {}
    d['image'] = pygame.image.load(filename)
    d['w'] = d['image'].get_width()
    d['h'] = d['image'].get_height()

    if width is not None:
        d['framew'] = width
    else:
        d['framew'] = d['w']

    if height is not None:
        d['frameh'] = height
    else:
        d['frameh'] = d['h']

#    d['framex'] = d['w'] // d['framew']
#    d['framey'] = d['h'] // d['frameh']
#
    _images[filename] = d
    return d

def wait():
    return

def clear(color=0):
    composer.fill(color)

def blit(source):
    Sprite(source, 0, 0, 0)

def sprite(source, x, y, frame):
    source['image'].set_colorkey(TRANSPARENT)
    framex = source['w'] // source['framew']
    xpos = frame % framex * source['framew']
    ypos = frame // framex * source['frameh']

    composer.blit(
            source['image'],(x,y),
            (xpos, ypos,source['framew'],source['frameh']))

def invertcolor(enabled):
    global inverted
    inverted = enabled

def map(tilemap, levelmap, offset_x, offset_y, x1, y1, x2, y2):
    return

def loadfont(sourcevar, startingcharvar, tilesize_xvar, tilesize_yvar):
    return

def char(char, x, y):
    return

def string(stringvar, origin_x, origin_y):
    return

def textbox(stringvar, origin_x, origin_y, w, h):
    return

def setclip(clipx1, clipy1, clipx2, clipy2):
    return

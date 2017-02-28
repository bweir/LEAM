import os, sys

import pygame
from pygame.locals import *

res_x = 128
res_y = 64

BLACK = (0,0,0)
WHITE = (255,255,255)
TRANSPARENT = (255,0,255)
GRAY = (128,128,128)

composer = None
inverted = False

def Start():
    global composer
    composer = pygame.Surface((res_x, res_y))
    return composer

def WaitToDraw():
    return

def ClearScreen(color):
    composer.fill(color)

def Blit(source):
    Sprite(source, 0, 0, 0)

def Sprite(source, x, y, frame):
    source['image'].set_colorkey(TRANSPARENT)
    xpos = frame % (source['image'].get_width()/source['width']) * source['width']
    ypos = frame / (source['image'].get_width()/source['width']) * source['height']

    composer.blit(
            source['image'],
            (x,y),
            (xpos, ypos,source['width'],source['height']))

def InvertColor(enabled):
    global inverted
    inverted = enabled

def Map(tilemap, levelmap, offset_x, offset_y, x1, y1, x2, y2):
    return

def LoadFont(sourcevar, startingcharvar, tilesize_xvar, tilesize_yvar):
    return

def PutChar(char, x, y):
    return

def PutString(stringvar, origin_x, origin_y):
    return

def TextBox(stringvar, origin_x, origin_y, w, h):
    return

def SetClipRectangle(clipx1, clipy1, clipx2, clipy2):
    return

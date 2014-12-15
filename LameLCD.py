#/usr/bin/env python
import os, sys

import pygame
from pygame.locals import *

SCREEN_W = 128
SCREEN_H = 64
BITSPERPIXEL = 2
SCREEN_H_BYTES = SCREEN_H / 8
SCREENSIZE_BYTES = SCREEN_W * SCREEN_H_BYTES * BITSPERPIXEL
TOTALBUFFER_BYTES = SCREENSIZE_BYTES
FULLSPEED = 40
HALFSPEED = 20
QUARTERSPEED = 10

SCALAR = 4

def Start():
    DISPLAYSURF = pygame.display.set_mode((
        SCREEN_W*SCALAR,
        SCREEN_H*SCALAR)
        )
    pygame.display.set_caption(sys.argv[0])

def DrawScreen():
    pygame.display.update()

def SetFrameLimit(frequency):
    return true

def InvertScreen(enabled):
    return true

def WaitForVerticalSync():
    return true

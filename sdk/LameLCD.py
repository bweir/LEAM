import os, sys

import pygame
from pygame.locals import *

SCREEN_W = 128
SCREEN_H = 64
BITSPERPIXEL = 2
FULLSPEED = 40
HALFSPEED = 20
QUARTERSPEED = 10

SCALAR = 4

composer = None
screen = None
inverted = False

clock = pygame.time.Clock()
speed = 0

def Start(framebuffer):
    global composer
    global screen
    screen = pygame.display.set_mode(
            (SCREEN_W*SCALAR,
                SCREEN_H*SCALAR))
    composer = framebuffer
    pygame.display.set_caption(sys.argv[0])

def DrawScreen():
    pygame.transform.scale(composer, 
            (SCREEN_W*SCALAR, 
                SCREEN_H*SCALAR),
            screen)

    if inverted:
        pixels = pygame.surfarray.pixels2d(screen)
        pixels ^= 2 ** 32 - 1
        del pixels

    pygame.display.update()
    if speed > 0:
        clock.tick(speed)

def SetFrameLimit(frequency):
    global speed
    speed = frequency
    return

def InvertScreen(enabled):
    global inverted
    inverted = enabled

def WaitForVerticalSync():
    return

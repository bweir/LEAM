"""
LameControl
***********
A tiny controller library for LameStation.

Usage
=====

``lame.control`` is easy to get started with.

>>> import lame.control as ctrl
>>> ctrl.start()

Call ``ctrl.update()`` to refresh the controls.

>>> ctrl.update()

Then you can use any commands.

>>> ctrl.a()
0
>>> ctrl.b()
1
>>> ctrl.left()
0
>>> ctrl.up()
1

``a`` and ``b`` are mapped to the keys ``z`` and ``x``.
"""

import sys

import pygame
from pygame.locals import *

from lame import fn

pygame.init()
keys = pygame.key.get_pressed()

def start():
    """Initialize lame.control."""
    return

def update():
    """Refresh key presses."""
    global keys
    pygame.event.pump()
    if pygame.event.peek():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    keys = pygame.key.get_pressed()

def a():
    """Get A key."""
    return keys[K_z]

def b():
    """Get B key."""
    return keys[K_x]

def left():
    """Get left arrow."""
    return keys[K_LEFT]

def right():
    """Get right arrow."""
    return keys[K_RIGHT]

def up():
    """Get up arrow."""
    return keys[K_UP]

def down():
    """Get down arrow."""
    return keys[K_DOWN]

def waitkey():
    """Wait for any key press."""
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return

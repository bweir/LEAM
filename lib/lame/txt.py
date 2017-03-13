from lame import gfx 
from lame import log

import textwrap

NL = 10
LF = 13

font = None

def load(filename, width, height, start=' '):
    global font
    font = gfx.load(filename, width, height)
    font['start'] = ord(start)
    return font

def char(c, x, y):
    gfx.sprite(font, x, y, ord(c) - font['start'])

def string(s, x, y):
    ox = x
    dx = font['framew']
    dy = font['frameh']
    for c in s:
        if c in '\n\r':
            y += dy
            x = ox
        elif c in (' '):
            x += dx
        else:
            char(c, x, y)
            x += dx

def box(s, x, y, w):
    w //= font['framew']
    string(textwrap.fill(s, w), x, y)

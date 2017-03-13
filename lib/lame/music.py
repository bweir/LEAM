from lame import log

import pygame
import sys

def start():
    pygame.init()

def load(filename):
    try:
        pygame.mixer.music.load(filename)
        log.info("Loaded music: "+filename)
    except pygame.error:
        log.error("Music not found: "+filename)
        sys.exit(1)

def play():
    pygame.mixer.music.play()

def loop():
    pygame.mixer.music.play(-1)

def stop():
    pygame.mixer.music.stop()

def playing():
    return pygame.mixer.music.get_busy()

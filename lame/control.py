import os, sys

import pygame
from pygame.locals import *

import lame.functions as fn      

pygame.init()

keys = pygame.key.get_pressed()

def Start():
    return

def Update():
    global keys
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()

def A():
    return keys[K_z]

def B():
    return keys[K_x]

def Left():
    return keys[K_LEFT]

def Right():
    return keys[K_RIGHT]

def Up():
    return keys[K_UP]

def Down():
    return keys[K_DOWN]

def WaitKey():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_z or event.key == K_x:
                    return
        fn.Sleep(20)


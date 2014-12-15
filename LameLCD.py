#/usr/bin/env python
import os, sys

import pygame
from pygame.locals import *

class LameLCD:

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
    
    def Start(self,framebuffer):
        self.screen = pygame.display.set_mode(
                (self.SCREEN_W*self.SCALAR,
                    self.SCREEN_H*self.SCALAR))
        self.composer = framebuffer
        pygame.display.set_caption(sys.argv[0])
        print "Bacon"
    
    def DrawScreen(self):
        pygame.transform.scale(self.composer, 
                (self.SCREEN_W*self.SCALAR, 
                    self.SCREEN_H*self.SCALAR),
                self.screen)
        print "lcd",self.composer
        pygame.display.update()
    
    def SetFrameLimit(self,frequency):
        return true
    
    def InvertScreen(self,enabled):
        return true
    
    def WaitForVerticalSync(self):
        return true

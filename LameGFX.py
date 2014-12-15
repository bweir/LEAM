#/usr/bin/env python
import os, sys

import pygame
from pygame.locals import *

class LameGFX:

    res_x = 128
    res_y = 64

    def Start(self):
        self.composer = pygame.Surface(
                (self.res_x, self.res_y), flags=HWSURFACE)
        return self.composer

    def WaitToDraw(self):
        return

    def ClearScreen(self,color):
        return

    def Blit(self,source):
        return

    def Sprite(self, source, x, y, frame):
        print source, source.get_rect()
        self.composer.blit(source, source.get_rect())
        print "composer",self.composer

    def InvertColor(self,enabled):
        return

    def Map(self,tilemap, levelmap, offset_x, offset_y, x1, y1, x2, y2):
        return

    def LoadFont(self, sourcevar, startingcharvar, tilesize_xvar, tilesize_yvar):
        return

    def PutChar(self,char, x, y):
        return

    def PutString(self,stringvar, origin_x, origin_y):
        return

    def TextBox(self,stringvar, origin_x, origin_y, w, h):
        return

    def SetClipRectangle(self,clipx1, clipy1, clipx2, clipy2):
        return

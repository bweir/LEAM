import os, sys
import random

import pygame
from pygame.locals import *

pygame.init()

import lame.lcd as lcd     
import lame.gfx as gfx     
import lame.control as ctrl    
import lame.functions as fn      
import gfx_tilemap as tilemap  
import gfx_frappy as player   
import gfx_frappybird as title    
import gfx_youdie as youdied  
import gfx_numbers as font     
import gfx_pressa as pressa   
import song_frappy as song     






PIPE_TOP = 3
PIPE_MID = 5
PIPE_BOT = 7
SKY = 1
SKYLINE = 0
BUSH = 2
FLOOR = 4
UNDER = 6


MAXPIPES = 8


#1, _JUMP, _DING, _ERRR


xoffset = None
xoffsetcounter = None
playerx = None
playery = None
speedx = None
speedy = None
flighttimeout = None
score = None


pipeon = [0]*MAXPIPES
pipex = [0]*MAXPIPES
pipey = [0]*MAXPIPES
pipeh = [0]*MAXPIPES
passed = [0]*MAXPIPES
pipe = None


intarray = [0]*4

def Main():
    lcd.Start(gfx.Start())
    lcd.SetFrameLimit(lcd.FULLSPEED)
    txt.Load(font.Addr(), "0", 4, 6)
    cognew(SFXEngine, SFXStack)
    clicked = 0
    while True:
        TitleScreen
        GameLoop
        GameOver

def TitleScreen():
    flightstate = 0
    xoffset = 0
    while not ctrl.A() and not ctrl.B():
        ctrl.Update()
        xoffset += 1
        gfx.Fill(gfx.WHITE)
        PutTileParallax(0,48,16,UNDER)
        PutTileParallax(xoffset,56,16,FLOOR)
        PutTileParallax(xoffset,40,8,BUSH)
        PutTileParallax(xoffset,24,4,SKYLINE)
        if flighttimeout > 0:
            flighttimeout -= 1
        else:
            flighttimeout = 20
            if flightstate:
                flightstate = 0
            else:
                flightstate = 1
        gfx.Sprite(player.Addr(), 56, 32, flightstate)
        gfx.Sprite(title.Addr(), 40, 4, 0)
        gfx.Sprite(pressa.Addr(),44,52,0)
        lcd.Draw()

def GameLoop():
    xoffset = 0
    died = 0
    tapped = 0
    playerx = 56
    playery = 32
    score = 0
    InitPipes
    while not died:
        ctrl.Update()
        gfx.Fill(gfx.WHITE)
        xoffset += 1
        PutTileParallax(0,48,16,UNDER)
        PutTileParallax(xoffset,56,16,FLOOR)
        PutTileParallax(xoffset,40,8,BUSH)
        PutTileParallax(xoffset,24,4,SKYLINE)
        ControlPipes
        HandlePlayer
        KeepScore
        lcd.Draw()

def GameOver():
    gfx.Sprite(youdied.Addr(),40,32,0)
    lcd.Draw()
    Errr
    fn.Sleep(1000)

def HandlePlayer():
    if ctrl.A():
        if not clicked:
            clicked = 1
            RunSound(_JUMP)
            flighttimeout = 10
            speedy = -9
    else:
        clicked = 0
        flighttimeout = 0
    if speedy < 32:
        speedy += 1
    playery += (speedy / 4)
    if playery > constant(60-16):
        speedy = 0
        died = 1
    if flighttimeout > 0:
        gfx.Sprite(player.Addr(), playerx, playery, 1)
        flighttimeout -= 1
    else:
        gfx.Sprite(player.Addr(), playerx, playery, 0)

def InitPipes():
    t = 0
    xoffset = 0
    pipe = 0
    for t in range(0, MAXPIPES-1):
        pipex[t] = 0
        pipey[t] = 0
        pipeh[t] = 0
        passed[t] = 0
        pipeon[t] = 0

def ControlPipes():
    t = 0
    ran = 0
    if xoffsetcounter > 0:
        xoffsetcounter -= 1
    else:
        ran = 0
        xoffsetcounter = 32 + (random.getrandbits(32) & int("0x1F",0))
        pipex[pipe] = xoffset+lcd.SCREEN_W
        pipey[pipe] = 16 + (random.getrandbits(32)  & int("0xF",0))
        pipeh[pipe] = 16
        passed[pipe] = 0
        pipeon[pipe] = 1
        pipe = (pipe+1) & int("0x7",0)
    for t in range(0, MAXPIPES-1):
        if pipeon[t]:
            PutPipeOpening(pipex[t]-xoffset, pipey[t], pipeh[t])
            if playerx+xoffset > pipex[t]+16 and not passed[t]:
                passed[t] = 1
                score += 1
                RunSound(_DING)

def PutPipeOpening(x,y,h):
    bound_upper = 0
    bound_lower = 0
    dy = 0
    t = 0
    bound_upper = y-h-16
    bound_lower = y+h
    dy = bound_upper
    if dy > 0:
        for t in range(0, dy, 16):
            PutTile(x,t,PIPE_MID)
    dy = bound_lower + 16
    if dy < 64:
        for t in range(dy, 64, 16):
            PutTile(x,t,PIPE_MID)
    PutTile(x,bound_upper,PIPE_BOT)
    PutTile(x,bound_lower,PIPE_TOP)
    if not playerx + word[player.Addr()][1] < x and not playerx > x+16 and playery < -word[player.Addr()][2]:
            died = 1
    if fn.TestBoxCollision(playerx, playery, word[player.Addr()][1], word[player.Addr()][2], x, 0, 16, bound_upper+16):
        died = 1
    if fn.TestBoxCollision(playerx, playery, word[player.Addr()][1], word[player.Addr()][2], x, bound_lower, 16, 64):
        died = 1

def PutTileParallax(x, y, speed, tile):
    t = 0
    dx = 0
    dx = 16/speed - 1
    x = (x >> dx) & int("0xF",0)
    for t in range(0, 128, 16):
        PutTile(t-x, y, tile)

def PutTile(x, y, tile):
    gfx.Sprite(tilemap.Addr(), x, y, tile)

def KeepScore():
    tmp = 0
    tmp = score
    intarray[2] = 48+(tmp % 10)
    tmp /= 10
    intarray[1] = 48+(tmp % 10)
    tmp /= 10
    intarray[0] = 48+(tmp % 10)
    intarray[3] = 0
    txt.Str(intarray, 0, 0)

def SFXEngine():
    while True:
        if SFXplay == _JUMP:
            Jump(3)
        elif SFXplay == _DING:
            Ding(2)
        elif SFXplay == _ERRR:
            Errr()
        SFXstop = 0

def RunSound(sound):
    if SFXplay:
        SFXstop = 1
    while True:
        if not SFXstop:
            break
    SFXplay = sound




#Main()
#while True:
#    for event in pygame.event.get():
#        if event.type == QUIT:
#             pygame.quit()
#             sys.exit()

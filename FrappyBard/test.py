from lame import gfx
from lame import ctrl
from lame import txt
from lame import log

import random

gfx.start(title='Frappy Bard')
gfx.limit(gfx.FULLSPEED)

tilemap = gfx.load('gfx/tilemap.png', 16, 16)
player = gfx.load('gfx/frappy.png', 16, 16)

title = gfx.load('gfx/frappybird.png')
youdied = gfx.load('gfx/youdie.png')
pressa = gfx.load('gfx/pressa.png')

font = txt.load('gfx/font4x6.png', 4, 6, ' ')

#log.error("This is a message")
#log.debug("This is a message")
#log.info("This is a message")
#log.warn("This is a message")

PIPE_TOP = 3
PIPE_MID = 5
PIPE_BOT = 7
SKY = 1
SKYLINE = 0
BUSH = 2
FLOOR = 4
UNDER = 6


MAXPIPES = 8


xoffset = 0
xoffsetcounter = 0
playerx = 0
playery = 0
speedx = 0
speedy = 0
flighttimeout = 0
score = 0


pipeon = [0]*MAXPIPES
pipex = [0]*MAXPIPES
pipey = [0]*MAXPIPES
pipeh = [0]*MAXPIPES
passed = [0]*MAXPIPES
pipe = 0
    
clicked = 0

intarray = [0]*4


def put_parallax_tile(x, y, speed, tile):
    t = 0
    dx = 16 // speed - 1
    x = (x >> dx) & int("0xF",0)
    for t in range(0, 144, 16):
        put_tile(t-x, y, tile)

def put_tile(x, y, tile):
    gfx.sprite(tilemap, x, y, tile)

def title_screen():
    global flighttimeout
    flightstate = 0
    xoffset = 0

    while not ctrl.a() and not ctrl.b():
        ctrl.update()
        xoffset += 1

        gfx.clear(0xb3ffff)
        put_parallax_tile(0,48,16,UNDER)
        put_parallax_tile(xoffset,56,16,FLOOR)
        put_parallax_tile(xoffset,40,8,BUSH)
        put_parallax_tile(xoffset,24,4,SKYLINE)

        if flighttimeout > 0:
            flighttimeout -= 1
        else:
            flighttimeout = 20
            if flightstate:
                flightstate = 0
            else:
                flightstate = 1

        gfx.sprite(player, 56, 32, flightstate)
        gfx.sprite(title, 40, 4, 0)
        gfx.sprite(pressa,44,52,0)
        gfx.draw()

def game_loop():
    global xoffset
    global died, tapped
    global playerx, playery
    global score
    xoffset = 0
    died = 0
    tapped = 0
    playerx = 56
    playery = 32
    score = 0
    init_pipes()

    while not died:
        ctrl.update()
        gfx.clear(0xb3ffff)
        xoffset += 1
        put_parallax_tile(0,48,16,UNDER)
        put_parallax_tile(xoffset,56,16,FLOOR)
        put_parallax_tile(xoffset,40,8,BUSH)
        put_parallax_tile(xoffset,24,4,SKYLINE)
        control_pipes()
        handle_player()
        keep_score()
        gfx.draw()

def game_over():
    gfx.sprite(youdied,40,32,0)
    gfx.draw()
    fn.sleep(1000)


def init_pipes():
    t = 0
    global xoffset
    global pipe
    global pipex, pipey, pipeh, passed, pipeon
    xoffset = 0
    pipe = 0
    for t in range(0, MAXPIPES-1):
        pipex[t] = 0
        pipey[t] = 0
        pipeh[t] = 0
        passed[t] = 0
        pipeon[t] = 0

def control_pipes():
    t = 0
    ran = 0
    global xoffset
    global pipe
    global pipex, pipey, pipeh, passed, pipeon

    global xoffsetcounter
    global score

    if xoffsetcounter > 0:
        xoffsetcounter -= 1
    else:
        ran = 0
        xoffsetcounter = 32 + (random.getrandbits(32) & int("0x1F",0))
        pipex[pipe] = xoffset+gfx.SCREEN_W
        pipey[pipe] = 16 + (random.getrandbits(32)  & int("0xF",0))
        pipeh[pipe] = 16
        passed[pipe] = 0
        pipeon[pipe] = 1
        pipe = (pipe+1) & int("0x7",0)

    for t in range(0, MAXPIPES-1):
        if pipeon[t]:
            put_pipe_opening(pipex[t]-xoffset, pipey[t], pipeh[t])
            if playerx+xoffset > pipex[t]+16 and not passed[t]:
                passed[t] = 1
                score += 1

def put_pipe_opening(x,y,h):
    bound_upper = y-h-16
    bound_lower = y+h
    dy = bound_upper

    if dy > 0:
        for t in range(0, dy, 16):
            put_tile(x,t,PIPE_MID)
    dy = bound_lower + 16
    if dy < 64:
        for t in range(dy, 64, 16):
            put_tile(x,t,PIPE_MID)

    put_tile(x,bound_upper,PIPE_BOT)
    put_tile(x,bound_lower,PIPE_TOP)

    if not playerx + player['framew'] < x and not playerx > x+16 and playery < -player['frameh']:
            died = 1
#    if fn.TestBoxCollision(playerx, playery, word[player.Addr()][1], word[player.Addr()][2], x, 0, 16, bound_upper+16):
#        died = 1
#    if fn.TestBoxCollision(playerx, playery, word[player.Addr()][1], word[player.Addr()][2], x, bound_lower, 16, 64):
#        died = 1

def keep_score():
    txt.string(str(score).zfill(3), 0, 0)
#    txt.string("this is the score\nwut!!! "+str(343), 20, 0)
#    txt.box("oodf osdf iosdfio jsdf sdf"
#            "iodfdsjfo sdf ids ijsdf ojdsf"
#            "josdf sdf sdf ojsdf jos fsdf", 0, 0, 128)

def handle_player():
    global clicked
    global playerx, playery
    global speedx, speedy
    global flighttimeout
    if ctrl.a():
        if not clicked:
            clicked = 1
            flighttimeout = 10
            speedy = -9
    else:
        clicked = 0
        flighttimeout = 0

    if speedy < 32:
        speedy += 1
    playery += (speedy // 4)
    if playery > 60-16:
        speedy = 0
        died = 1
    if flighttimeout > 0:
        gfx.sprite(player, playerx, playery, 1)
        flighttimeout -= 1
    else:
        gfx.sprite(player, playerx, playery, 0)


def main():
    stuff = 0
    x = 0
    y = 0

    while True:
        title_screen()
        game_loop()
        game_over()
    
    ctrl.waitkey()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        pass

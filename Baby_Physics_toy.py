"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random
import pyHook 
import os

key_map = { 27:1, 112:3, 113:4, 114:5, 115:6, 116:7, 117:8, 118:9, 119:10, 120:11, 121:12, 122:13, 
                44:14, 145:18, 19:19, 
            192:1, 49:2, 50:3, 51:4, 52:5, 53:6, 54:7, 55:8, 56:9, 57:10, 48:11, 189:12, 187:13, 8:15, 
                45:17, 36:18, 33:19, 
                    144:21, 111:22, 106:23, 109:24,
            9:1, 81:3, 87:4, 69:5, 82:6, 84:7, 89:8, 85:9, 73:10, 79:11, 80:12, 219:13, 221:14, 220:15, 
                46:17, 35:18, 34:19, 
                    103:21, 104:22, 105:23, 107:24,
                    36:17, 103:19,
            20:1, 65:3, 83:4, 68:5, 70:6, 71:7, 72:8, 74:9, 75:10, 76:11, 186:12, 222:13, 13:15, 
                    100:21, 101:22, 102:23, 107:24,
                    12:18,
            160:1, 90:3, 88:4, 67:5, 86:6, 66:7, 78:8, 77:9, 188:10, 190:11, 191:12, 161:15, 
                38:18,  
                    97:21, 98:22, 99:23, 13:24,
                    35:21, 34:24,
            162:1, 91:2, 164:3, 32:7, 165:11, 93:14, 163:15, 
                37:17, 40:18, 39:19,   
                    96:21, 110:23,
                    45:21.
}

keys_down = {}

## Balls
balls = []

def get_x_from_key(key):
    if key != 177:
        if key in key_map:
            print("Key: %s" % key)
            return key_map[key]
        else:
            print("Invalid Key: %s" % key)
            return random.randint(1,24)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos>1279:
        pos = 1279
    if pos<0:
        pos = 0

    if pos <= 255:
        r = 255-pos
        g = 0
        b = 255
    else:
        pos = pos-256
        if pos <= 255:
            r = 0
            g = pos
            b = 255
        else:
            pos = pos-256
            if pos <= 255:
                r = 0
                g = 255
                b = 255-pos
            else:
                pos = pos-256
                if pos <= 255:
                    r = pos
                    g = 255
                    b = 0
                else:
                    pos = pos-256
                    if pos <= 255:
                        r = 255
                        g = 255-pos
                        b = 0
                    else:
                        r = 255
                        g = 0 
                        b = 0
            
    return (r, g, b, 255)
    
def printEvent(event):
    print('MessageName:',event.MessageName)
    print('Message:',event.Message)
    print('Time:',event.Time)
    print('Window:',event.Window)
    print('WindowName:',event.WindowName)
    print('Ascii:', event.Ascii, chr(event.Ascii))
    print('Key:', event.Key)
    print('KeyID:', event.KeyID)
    print('ScanCode:', event.ScanCode)
    print('Extended:', event.Extended)
    print('Injected:', event.Injected)
    print('Alt', event.Alt)
    print('Transition', event.Transition)
    print('---')

def OnKeyboardDown(event):
    #print("KeyDown: %s"  % event.KeyID)
    #printEvent(event)
    global balls
    
    random.choice(sounds).play()
    key_pos = get_x_from_key(event.KeyID)
    print("key_pos: %s" % key_pos)
    scale = int(X_DIM/25)
    print("scale: %s" % scale)
    mass = 10
    radius = RAD
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = key_pos * scale
    print("x: %s" % x)
    body.position = x, Y_DIM
    shape = pymunk.Circle(body, radius, (0,0))
    shape.elasticity = 0.95
    shape.friction = 0.9
    space.add(body, shape)
    balls.append(shape)
    
    keys_down[event.KeyID] = 1
    return False
        
def OnKeyboardUp(event):
    #print("KeyUp")
    #printEvent(event)
    keys_down[event.KeyID] = 0
    print(event.Key.lower())
    
    return False    # block these keys
     
def check_keydown(KeyID):
    if KeyID in keys_down:
        if keys_down[KeyID] == 1:
            return True
    
    return False
    
def check_secret_keys():
    #http://cherrytree.at/misc/vk.htm
    #162 left control
    #160 left shift
    #164 left alt
    #up arrow
    if check_keydown(162) and check_keydown(160) and check_keydown(164) and check_keydown(38):
        return True
    return False
mult = 1
X_DIM = 1280 * mult
Y_DIM = 720 * mult
RAD = 25 * mult
    
    
# create a hook manager
hm = pyHook.HookManager()
# watch for all keyboard events
hm.KeyDown = OnKeyboardDown
hm.KeyUp = OnKeyboardUp
# set the hook
hm.HookKeyboard()
    
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
#,pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
#screen = pygame.display.set_mode((X_DIM, Y_DIM),pygame.FULLSCREEN )

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (1700,0)
screen = pygame.display.set_mode((X_DIM,Y_DIM),pygame.NOFRAME) 

screen.fill((255,255,255,255))
clock = pygame.time.Clock()
running = True

### Physics stuff
space = pymunk.Space()
space.gravity = (0.0, -900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
   
### walls
static_body = space.static_body
static_lines = []

for line in range(10):
    x1 = random.randint(RAD*5,X_DIM-(RAD*5))
    y1 = random.randint(RAD*5,int(Y_DIM/1.5))
    x2 = x1 + random.randint(RAD * 2, RAD * 10)
    y2 = y1 + random.randint(-(RAD*2), RAD * 2)
    static_lines.append(pymunk.Segment(static_body, (x1, y1), (x2, y2), 0.0))
    
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 0.9
space.add(static_lines)

ticks_to_next_ball = 10
last_keypressed = []

sounds = []
for x in range(5):
    sounds.append(pygame.mixer.Sound("smb_coin%d.wav" % x))

while running:
    got_key = 0
    pygame.event.pump()
        
    if check_secret_keys():
        print("")
        print("")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("")
        print("")
        running=False
            
    
    ### Clear screen
    screen.fill((1,1,1,255),special_flags=BLEND_ADD)
    
    ### Draw stuff
    balls_to_remove = []
    for ball in balls:
        if ball.body.position.y < -RAD: 
            balls_to_remove.append(ball)
        else:
            color = int(ball.body.kinetic_energy / 5000)
            #print(wheel(color))
            ball.color = wheel(color)

    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)

    space.debug_draw(draw_options)

    ### Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)
    
    ### Flip screen
    pygame.display.update()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

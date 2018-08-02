#!/usr/bin/env python

import pygame
import time
import sys
import random

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos>1280:
        pos = 1280

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
            
    return (r, g, b)

pygame.init()
pygame.mixer.init()

sounds = []
for x in range(5):
    sounds.append(pygame.mixer.Sound("smb_coin%d.wav" % x))
    
print(pygame.display.list_modes())

screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
#screen = pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.mouse.set_visible(False)
pygame.draw.rect(screen, (255,0,0), [0, 0, 1024, 768])
pygame.display.update()

running=True
clock = pygame.time.Clock()

last_key = []


while running==True:
    got_key = 0
    pygame.event.pump()
    keypressed = pygame.key.get_pressed()
    
    for key in range(len(keypressed)):
        if keypressed[key]!=0 and last_key[key]==0:
            print("Got key: %d" % key)
            got_key = key
            random.choice(sounds).play()
            
    last_key = keypressed
            
    if got_key != 0:
        color = wheel((got_key * 10) % 1280)
        screen.fill(color)
        pygame.display.flip()

    #exit if pressing ctrl+alt+shift+up
    if keypressed[pygame.K_UP]:
        mods=pygame.key.get_mods()
        print("Got up, mods: %d" % mods)
        if mods==321:
            running=False

#sometimes pygame wouldn't exit fullscreen correctly
pygame.display.set_mode((320, 240))
time.sleep(2)
pygame.quit()
time.sleep(2)
sys.exit()

__author__ = 'starlord'
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600,400), 0, 32)
x, y = (300, 200)

while True:
    for event in pygame.event.get(): #this will close the window
        if event.type == QUIT:
            exit()

    key_pressed = pygame.key.get_pressed() #key handling
    if key_pressed[K_UP]:
        y -= 5
    elif key_pressed[K_DOWN]:
        y += 5
    elif key_pressed[K_LEFT]:
        x -= 5
    elif key_pressed[K_RIGHT]:
        x += 5

    background = pygame.surface.Surface((600,400)).convert()
    background.fill((0,0,0))
    screen.blit(background, (0,0))

    #large static rectangle
    pygame.draw.rect(screen, (0,0,255),[400,200,60,80])

    #lines to detect collision for static
    pygame.draw.line(screen, (255,0,255), (0, 200), (0, 200+80), 10)
    pygame.draw.line(screen, (255,0,255), (400, 0), (400+60, 0), 10)

    #lines to detect collision for moving
    pygame.draw.line(screen, (255,50,2), (0, y), (0, y+50), 10)
    pygame.draw.line(screen, (255,50,2), (x, 0), (x+50, 0), 10)

    #moving entity
    pygame.draw.rect(screen, (255,255,0),[x,y,50, 50])
    pygame.display.update()


#-----------------------------------------------------------------------------
#function to check collisions using SAT(separating axis theorem)
def axis_overlap(p1, length1, p2, length2):
    collided = False
    if (p1 > p2):
        if (length1+length2 > p1+length1-p2):
            collided = True
    elif (p2 > p1):
        if (length1+length2 > p2+length2-p1):
            collided = True
    elif(p1==p2):
        collided = True
    return collided
#------------------------------------------------------------------------------
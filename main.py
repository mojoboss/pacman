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
        y -= 1
    elif key_pressed[K_DOWN]:
        y += 1
    elif key_pressed[K_LEFT]:
        x -= 1
    elif key_pressed[K_RIGHT]:
        x += 1

    background = pygame.surface.Surface((600,400)).convert()
    background.fill((0,0,0))
    screen.blit(background, (0,0))

    pygame.draw.rect(screen, (255,255,0),[x,y,16,16])
    pygame.display.update()

__author__ = 'starlord'

import pygame
from pygame.locals import *

from pacman import Pacman
from tiles import Tile

pygame.init()
SCREEN_SIZE = (900, 600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))


pacman = Pacman((50,50), [500,200])
tile = Tile((150,150), [150,100])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    pacman.move()
    pacman.collide(tile)
    screen.blit(background, (0,0))
    tile.draw(screen)
    pacman.draw(screen)
    pygame.display.update()

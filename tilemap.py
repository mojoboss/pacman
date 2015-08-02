__author__ = 'starlord'

import pygame
import numpy
from tiles import Tile
from pacman import Pacman
from pygame.locals import *


pygame.init()
layout = numpy.loadtxt('tilemap_test.txt', dtype=str)
row, col = layout.shape
width, height = (16, 16)

SCREEN_SIZE = (width*row, height*col)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

tiles = []

for i in range(row):
    for j in range(col):
        value = layout[i][j]
        if (value != '0'):
            pos = (i*width, j*height)
            tiles.append(Tile((width, height), pos))

pacman = Pacman((width-6,height-6), [4*width,2*height])


background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))
    for t in tiles:
        t.draw(screen)
    pacman.move()
    for t in tiles:
        pacman.collide(t)
    pacman.draw(screen)
    pygame.display.update()

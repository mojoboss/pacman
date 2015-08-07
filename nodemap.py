__author__ = 'starlord'

import pygame
from pygame.locals import *
from nodegroup import NodeGroup
from pacman import Pacman

from time import sleep
pygame.init()
width, height = (32, 32)
screen = pygame.display.set_mode((10*width, 10*height), 0, 32)
background = pygame.surface.Surface((10*width,10*height)).convert()
background.fill((0,0,0))

nodegrp = NodeGroup(width, height)
nodes = nodegrp.createNodeList('nodemap_test.txt')



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))
    for node in nodes:
        pygame.draw.circle(screen,(255,0,0),node.position.toTuple(), 10)
    for node in nodes:
        for nextnode in node.neighbors:
            pygame.draw.line(screen,(255,255,255),node.position.toTuple(), nextnode.position.toTuple(), 2)

    pygame.display.update()

__author__ = 'starlord'

import pygame
from pygame.locals import *
from nodegroup import NodeGroup
from pacman import Pacman
from tilegroup import Tilegroup
from time import sleep

pygame.init()
width, height = (32, 32)

screen = pygame.display.set_mode((10*width, 10*height), 0, 32)
background = pygame.surface.Surface((10*width,10*height)).convert()
background.fill((0,0,0))
filename = 'nodemap_test.txt'

tilegrp = Tilegroup(width, height)
tiles = tilegrp.createTileList(filename)

nodegrp = NodeGroup(width, height)
nodes = nodegrp.createNodeList(filename)

pacman = Pacman((width,height), [nodes[3].position.x, nodes[3].position.y])

while True:
    #sleep(0.01)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))

    for t in tiles:
        t.draw(screen)

    pacman.draw(screen)
    pacman.update(nodes)

    pygame.display.update()


'''
#code to draw the node graph
    for node in nodes:
        pygame.draw.circle(screen,(255,0,0),node.position.toTuple(), 10)
    for node in nodes:
        for nextnode in node.neighbors:
            pygame.draw.line(screen,(255,255,255),node.position.toTuple(), nextnode.position.toTuple(), 2)
'''
__author__ = 'starlord'

import pygame
from pygame.locals import *
import numpy
from nodegroup import NodeGroup
from pacman import Pacman
from ghost import Ghost
from tilegroup import Tilegroup
from time import sleep

def getRowCol(filename):
        layout = numpy.loadtxt(filename, dtype=str)
        c, r = layout.shape
        return r, c

pygame.init()
width, height = (16, 16)
filename = 'tilemap_test.txt'
r, c = getRowCol(filename)
screen = pygame.display.set_mode((r*width, c*height), 0, 32)
background = pygame.surface.Surface((r*width,c*height)).convert()
background.fill((0,0,0))

#code to add tiles in the screen
tilegrp = Tilegroup(width, height)
tiles = tilegrp.createTileList(filename)

#nodes added, not displayed on the screen, only for navigation purpose
nodegrp = NodeGroup(width, height)
nodes = nodegrp.createNodeList(filename)

#ghost added
ghost1 = Ghost(nodes[20], (255, 0, 0), (width,height), [nodes[20].position.x, nodes[20].position.y])
ghost2 = Ghost(nodes[7], (155, 0, 250), (width,height), [nodes[7].position.x, nodes[7].position.y])

pacman = Pacman(nodes[0], (width,height), [nodes[3].position.x, nodes[3].position.y])

while True:
    #sleep(0.01)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))

    for t in tiles:
        t.draw(screen)

    ghost1.draw(screen)
    ghost1.move(pacman.pos, nodes)
    ghost2.draw(screen)
    ghost2.move(pacman.pos, nodes)

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
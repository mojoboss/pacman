__author__ = 'starlord'

import pygame
from pygame.locals import *
import numpy
from nodegroup import NodeGroup
from pacman import Pacman
from ghost import Ghost
from tilegroup import Tilegroup
from coingroup import Coingroup
from time import sleep

def getRowCol(filename):
        layout = numpy.loadtxt(filename, dtype=str)
        c, r = layout.shape
        return r, c

pygame.init()
width, height = (16, 16)
filename = 'mazes/tenbyten.txt'
filecoin = 'mazes/tenbytencoin.txt'
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

#adding coins to our maze
coingrp = Coingroup(width)
coins = coingrp.createCoinList(filecoin)

#ghost added
ghost1 = Ghost(0.1, nodes[5], (255, 0, 0), (width,height), [nodes[5].position.x, nodes[5].position.y])
#pacman added
pacman = Pacman(nodes[1], (width,height), [nodes[1].position.x, nodes[1].position.y])
count=0
while True:
    #++++
    #count+=1
    #if count == 1000:
    #    ghost1.scatter_ghost()
    #elif count == 2000:
    #    ghost1.scatter_ghost()
    #    count = 0
    #++++
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))

    for t in tiles:
        t.draw(screen)

    for c in coins:
        c.draw(screen)

    for c in coins:
        if (pacman.coin_collide(c)):
            pygame.mixer.music.load('sounds/sound.wav')
            pygame.mixer.music.play(0)
            coins.remove(c)

    ghost1.draw(screen)
    ghost1.move(pacman.currentnode, nodes, 'bfs')
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
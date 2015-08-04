__author__ = 'starlord'
import pygame
from pygame.locals import *
from nodes import Node
from pacman import Pacman

pygame.init()
width, height = (32, 32)
screen = pygame.display.set_mode((10*width, 10*height), 0, 32)
background = pygame.surface.Surface((10*width,10*height)).convert()
background.fill((0,0,0))
node0 = Node((1,2), width, height)
node1 = Node((4,2), width, height)
node2 = Node((8,2), width, height)
node3 = Node((1,6), width, height)
node4 = Node((4,6), width, height)
node5 = Node((7,6), width, height)
node6 = Node((1,8), width, height)
node7 = Node((4,8), width, height)
nodes = [node0, node1, node2, node3, node4, node5, node6, node7]
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))
    for node in nodes:
        pygame.draw.circle(screen,(255,0,0),node.position.toTuple(), 10)
    pygame.display.update()

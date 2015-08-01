__author__ = 'starlord'
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600,400), 0, 32)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    pygame.display.update()

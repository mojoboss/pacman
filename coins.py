__author__ = 'starlord'
from entity import AbstractEntity
import pygame
#-----------------------------------------------------------------------------
#coin class
class Coin(object):
    def __init__(self, radius, pos=(0,0)):
        self.radius = radius/4
        self.pos = (pos[0]+8, pos[1]+8)
        self.COLOR = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR , self.pos, self.radius)
#-----------------------------------------------------------------------------
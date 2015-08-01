__author__ = 'starlord'
import pygame

#-----------------------------------------------------------------------------
#Tile class
class Tile(object):
    def __init__(self, dim, pos=[0,0]):
        self.dim = dim
        self.pos = pos
        self.COLOR = (255,0,0)

    def draw(self, screen):
        values = list(self.pos)+list(self.dim)
        pygame.draw.rect(screen, self.COLOR, values)
#-----------------------------------------------------------------------------

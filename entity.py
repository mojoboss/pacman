__author__ = 'starlord'
import pygame
from vectors import Vector2D

# Parent class for Pacman and Tile
class AbstractEntity(object):
    def __init__(self, dim, pos=(0,0)):
        self.dim = dim
        self.pos = Vector2D(pos[0], pos[1])
        self.COLOR = (0,0,0)

    def draw(self, screen):
        values = list(self.pos.toTuple()) + list(self.dim)
        pygame.draw.rect(screen, self.COLOR, values)
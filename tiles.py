__author__ = 'starlord'
import pygame
from entity import AbstractEntity

#-----------------------------------------------------------------------------
#Tile class
class Tile(AbstractEntity):
    def __init__(self, dim, pos=[0,0]):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = (0, 140, 0)
#-----------------------------------------------------------------------------

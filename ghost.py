__author__ = 'starlord'
import pygame
from pygame.locals import *
from entity import AbstractEntity
from vectors import Vector2D

UP = Vector2D(0,-1)
DOWN = Vector2D(0,1)
LEFT = Vector2D(-1,0)
RIGHT = Vector2D(1,0)

class Ghost(AbstractEntity):
    def __init__(self, node, color, dim, pos=(0,0)):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = color
        self.direction = Vector2D(0, 0)
        self.speed = 0.80
        self.currentnode = node
        self.moving = False

    def move(self, pacpos, nodelist):

        new_node = self.find_node(nodelist)
        if(new_node):
            self.currentnode = new_node
            self.moving = False
        if (not self.moving):
            node = self.currentnode
            min_dist = Vector2D.magnitude(node.neighbors[0].position-pacpos)
            index = 0
            for i in range(len(node.neighbors)):
                n = node.neighbors[i]
                mdist = Vector2D.magnitude(n.position-pacpos)
                if (mdist <= min_dist):
                    index = i
            self.direction = node.directions[index]
            self.moving = True

        self.pos += self.direction*self.speed

    def find_node(self, nodelist):
         for n in nodelist:
            if Vector2D.magnitude(self.pos-n.position) <= 0.1:
                return n
         return None

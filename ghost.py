__author__ = 'starlord'
import pygame
from pygame.locals import *
from entity import AbstractEntity
from vectors import Vector2D
from locatePacman import search_pacnode
UP = Vector2D(0,-1)
DOWN = Vector2D(0,1)
LEFT = Vector2D(-1,0)
RIGHT = Vector2D(1,0)

class Ghost(AbstractEntity):
    def __init__(self, node, color, dim, pos=(0,0)):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = color
        self.direction = Vector2D(0, 0)
        self.speed = 0.40
        self.currentnode = node
        self.moving = False

    def move(self, pacnode, nodelist):
        new_node = self.find_node(nodelist)
        if(new_node):
            self.currentnode = new_node
            self.moving = False
        if (not self.moving):
            node = self.currentnode
            map = search_pacnode(node, pacnode)
            child = pacnode
            parent = pacnode
            while True:
                parent = map[child]
                if (parent == node):
                    break
                else:
                    child = parent
            direct = child.position - parent.position
            direct = direct.normalize()
            self.direction = direct
            self.moving = True

        self.pos += self.direction*self.speed

    def find_node(self, nodelist):
         for n in nodelist:
            if Vector2D.magnitude(self.pos-n.position) <= 0.1:
                return n
         return None

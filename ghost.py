__author__ = 'starlord'
from entity import AbstractEntity
from vectors import Vector2D
from locatePacman import *
import pygame

UP = Vector2D(0,-1)
DOWN = Vector2D(0,1)
LEFT = Vector2D(-1,0)
RIGHT = Vector2D(1,0)

class Ghost(AbstractEntity):
    def __init__(self, speed, node, color, dim, pos=(0,0)):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = color
        self.direction = Vector2D(0, 0)
        self.speed = speed
        self.currentnode = node
        self.moving = False
        self.scatter = False
        self.rand_move_count = 1
    def move(self, pacnode, nodelist, alg):
        new_node = self.find_node(nodelist)
        if(new_node):
            self.currentnode = new_node
            self.moving = False
        if (not self.moving):
            node = self.currentnode
            keyerrorFlag = False
            #this is to catch keyerror exception, as child key is not present always
            try:
                map = search_pacnode_by_alg(node, pacnode, alg)
                child = pacnode
                parent = pacnode
                while True:
                    parent = map[child]
                    if (parent == node):
                        break
                    else:
                        child = parent
            except:
                keyerrorFlag = True

            if not keyerrorFlag:
                direct = child.position - parent.position
                direct = direct.normalize()
                self.direction = direct
            else:
                self.direction = Vector2D(0, 0)
            self.moving = True

        self.pos += self.direction*self.speed

    def find_node(self, nodelist):
         for n in nodelist:
            if Vector2D.magnitude(self.pos-n.position) <= 0.1:
                return n
         return None

    #METHOD FOR SCATTERING GHOSTS
    def scatter_ghost(self):
        if self.scatter == False:
            self.scatter = True
            return None
        elif self.scatter == True:
            self.scatter = False
            return None

    #Method for randomised ghost movement
    def random_ghost_movement(self):
        self.rand_move_count += 1
        if self.rand_move_count == 200:
            self.scatter_ghost()
            self.rand_move_count = 0

    #without calling this method(and just calling move), just keeping the speed of ghost 0.4 also gives sacttering
    #effect as its too slow
    def ghost_movement(self, pacnode, nodelist, alg):
        if not self.scatter:
            self.move(pacnode, nodelist, alg)
        else:
            new_node = self.find_node(nodelist)
            if(new_node):
                self.currentnode = new_node
                self.moving = False
            if (not self.moving):
                node = self.currentnode
                from random import randint
                direct_index = randint(0, len(node.directions)-1)
                self.direction = node.directions[direct_index]
                self.moving = True
            self.pos += self.direction*self.speed

    #method to draw ghost image on the screen
    def draw(self, screen):
        img=pygame.image.load('images/ghos.bmp')
        screen.blit(img, (self.pos.x, self.pos.y))
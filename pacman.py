
__author__ = 'starlord'
import pygame
from pygame.locals import *
from entity import AbstractEntity
from vectors import Vector2D


UP = Vector2D(0, -1)
DOWN = Vector2D(0, 1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)
#-----------------------------------------------------------------------------
#pacman class
class Pacman(AbstractEntity):
     def __init__(self,node ,dim ,pos=(0,0)):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = (255,255,0)
        self.direction = Vector2D(0, 0)
        self.speed = 3.2
        self.currentnode = node
        self.moving = False
     #+++++
     def find_node(self, nodelist):
         for n in nodelist:
            if Vector2D.magnitude(self.pos-n.position) <= 0.1:
                return n
         return None
     #+++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     def update(self, nodelist, qdictionary, key, training):
         if training:
             qdirection = self.best_action(qdictionary, key)
             best_direction = Vector2D(qdirection)
             index = self.currentnode.directions.index(best_direction)
             self.currentnode = self.currentnode.neighbors[index]
             self.pos = self.currentnode.position
             return best_direction
         else:
             if self.moving == False:
                 qdirection = self.best_action(qdictionary, key)
                 best_direction = Vector2D(qdirection)
                 self.direction = best_direction
                 self.moving = True
             direction = self.direction
             if self.moving:
                 self.pos += self.direction*self.speed
             next_node = self.find_node(nodelist)
             if next_node:
                 self.currentnode = next_node
                 self.pos = self.currentnode.position
                 self.moving = False
                 return direction
             return None

         '''
         index = self.currentnode.directions.index(best_direction)
         self.currentnode = self.currentnode.neighbors[index]
         self.pos = self.currentnode.position
         return best_direction
         '''
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     #to find best action
     def best_action(self, qdictionary, key):
         maxi = -9999999999
         direct = None
         for k in qdictionary[key]:
             if qdictionary[key][k] > maxi:
                 maxi = qdictionary[key][k]
                 direct = k
         return direct

     #code to test interaction with coins using SAT(separating axis theorem)
     def coin_collide(self, other):
        xcollide = axis_overlap(self.pos.x, self.dim[0], other.pos[0]-8, other.radius*2)
        ycollide = axis_overlap(self.pos.y, self.dim[1], other.pos[1]-8, other.radius*2)
        return xcollide & ycollide
    #code to check interaction with ghosts
     def ghost_collide(self, other):
        xcollide = axis_overlap(self.pos.x, self.dim[0], other.pos.x, other.dim[0])
        ycollide = axis_overlap(self.pos.y, self.dim[1], other.pos.y, other.dim[1])
        return xcollide & ycollide

#-------------------------------------------------------------------------------------------------------------
#function to check collisions using SAT(separating axis theorem)
def axis_overlap(p1, length1, p2, length2):
    collided = False
    if (p1 > p2):
        if (length1+length2 > p1+length1-p2):
            collided = True
    elif (p2 > p1):
        if (length1+length2 > p2+length2-p1):
            collided = True
    elif(p1==p2):
        collided = True
    return collided
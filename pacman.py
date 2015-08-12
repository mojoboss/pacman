
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
        self.speed = 0.80
        self.currentnode = node

     def update(self, nodelist):
         #if pacman position is same as any node then detect for key pressing
         node = self.find_node(nodelist)
         if(node):
             self.currentnode = node
             key_pressed = pygame.key.get_pressed()
             if (key_pressed[K_UP] and UP in node.directions):
                 self.pos = node.position
                 self.direction = UP
             elif (key_pressed[K_DOWN] and DOWN in node.directions):
                 self.pos = node.position
                 self.direction = DOWN
             elif (key_pressed[K_LEFT] and LEFT in node.directions):
                 self.pos = node.position
                 self.direction = LEFT
             elif (key_pressed[K_RIGHT] and RIGHT in node.directions):
                 self.pos = node.position
                 self.direction = RIGHT
             #if no key is pressed and current direction is not available..
             elif(self.direction not in node.directions):
                 self.pos = node.position
                 self.direction = Vector2D(0, 0)

         #code to update position
         self.pos += self.direction*self.speed

         #code to move pacman in between nodes
         key_pressed = pygame.key.get_pressed()
         if (key_pressed[K_UP] and self.direction == DOWN or
            key_pressed[K_DOWN] and self.direction == UP or
            key_pressed[K_LEFT] and self.direction == RIGHT or
            key_pressed[K_RIGHT] and self.direction == LEFT):
            self.switchNodes()

     #finds the  node just crossed by pacman
     def find_node(self, nodelist):
         for n in nodelist:
            if Vector2D.magnitude(self.pos-n.position) <= 0.1:
                return n
         return None

    #function to reverse the direction of pacman in between nodes
     def switchNodes(self):
         self.direction *= -1

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

__author__ = 'starlord'
import pygame
from pygame.locals import *
from entity import AbstractEntity
from vectors import Vector2D


UP = Vector2D(0,-1)
DOWN = Vector2D(0,1)
LEFT = Vector2D(-1,0)
RIGHT = Vector2D(1,0)
#-----------------------------------------------------------------------------
#pacman class
class Pacman(AbstractEntity):
     def __init__(self, dim, pos=(0,0)):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = (255,255,0)
        self.direction = Vector2D(0, 0)
        self.speed = 0.80
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     def update(self, nodelist):
         #if pacman position is same as any node then detect for key pressing
         node = self.find_node(nodelist)
         if(node):
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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     #finds the  node just crossed by pacman
     def find_node(self, nodelist):
         for n in nodelist:
            if Vector2D.magnitude(self.pos-n.position) <= 0.1:
                return n
         return None

    #function to reverse the direction of pacman in between nodes
     def switchNodes(self):
         self.direction *= -1
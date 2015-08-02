__author__ = 'starlord'
import pygame
from pygame.locals import *
from entity import AbstractEntity

#-----------------------------------------------------------------------------
#pacman class
class Pacman(AbstractEntity):
    def __init__(self, dim, pos):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = (255,255,0)
        self.direction = 'LEFT'

    def collide(self, other):
        xcollide = axis_overlap(self.pos.x, self.dim[0], other.pos.x, other.dim[0])
        ycollide = axis_overlap(self.pos.y, self.dim[1], other.pos.y, other.dim[1])
        if xcollide & ycollide:
            if self.direction is 'UP':
                self.pos.y = other.pos.y+other.dim[1]
            elif self.direction is 'DOWN':
                self.pos.y = other.pos.y-self.dim[1]
            elif self.direction is 'LEFT':
                self.pos.x = other.pos.x+other.dim[0]
            elif self.direction is 'RIGHT':
                self.pos.x = other.pos.x-self.dim[0]

    def move(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            self.pos.y -= 2
            self.direction = 'UP'
        elif key_pressed[K_DOWN]:
            self.pos.y += 2
            self.direction = 'DOWN'
        elif key_pressed[K_LEFT]:
            self.pos.x -= 2
            self.direction = 'LEFT'
        elif key_pressed[K_RIGHT]:
            self.pos.x += 2
            self.direction = 'RIGHT'
        #print (self.pos.x, self.pos.y)
        #print '\n'

#----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
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
#------------------------------------------------------------------------------

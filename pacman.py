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
        self.vel_stack=[]

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
            self.vel_stack.pop()
            if self.vel_stack:
                self.direction = self.vel_stack[-1][1]


#test++++++++++++++++++++++++++++
    def set_direction(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            self.direction = 'UP'
        elif key_pressed[K_DOWN]:
            self.direction = 'DOWN'
        elif key_pressed[K_LEFT]:
            self.direction = 'LEFT'
        elif key_pressed[K_RIGHT]:
            self.direction = 'RIGHT'
        return self.direction

    def set_vel(self):
        direct = self.set_direction()
        if(direct == 'UP'):
            v= (0, -2)
        elif(direct == 'DOWN'):
            v= (0, 2)
        if(direct == 'LEFT'):
            v= (-2, 0)
        if(direct == 'RIGHT'):
            v= (2, 0)
        if (v, direct) not in self.vel_stack:
            self.vel_stack.append((v, direct))
        return self.vel_stack
#+++++++++++++++++++++++++++++++++++
    def move(self):
        vel = self.set_vel()
        v = vel[-1][0]
        self.pos.x += v[0]
        self.pos.y += v[1]
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

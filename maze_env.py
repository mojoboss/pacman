__author__ = 'starlord'
from vectors import Vector2D
from random import random
import math
class Environment:
    def __init__(self, pacman, ghosts, nodes, coins):
        self.pacman = pacman
        self.ghosts = ghosts
        self.nodes = nodes
        self.coins = coins
        self.qdictionary = {}
#--------------------------------------------------------------------------
    def set_params(self, pacman, ghosts, nodes, coins):
        self.pacman = pacman
        self.ghosts = ghosts
        self.nodes = nodes
        self.coins = coins
#--------------------------------------------------------------------------
    def nearest_ghost(self):
        min_ghost = None
        min_dist = Vector2D.magnitude(self.pacman.pos - self.ghosts[0].pos)
        for g in self.ghosts:
            dist = Vector2D.magnitude(self.pacman.pos - g.pos)
            if dist <= 128.0 and dist <= min_dist:
                min_ghost = g
                min_dist = dist
        return min_ghost
#--------------------------------------------------------------------------
    def nearest_coin(self):
        min_coin = None
        min_dist = Vector2D.magnitude(self.pacman.pos - Vector2D(self.coins[0].pos[0], self.coins[0].pos[1]))
        for c in self.coins:
            dist = Vector2D.magnitude(self.pacman.pos - Vector2D(c.pos[0], c.pos[1]))
            if dist <= min_dist:
                min_coin = c
                min_dist = dist
        return min_coin
#--------------------------------------------------------------------------
    #This method creates a unique state space key which is differen for all state-spaces
    def make_key(self):
        s0 = 0
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        s5 = 0
        s6 = 0
        s7 = 0
        s8 = 0
        s9 = 0
        directions  = self.pacman.currentnode.directions
        if Vector2D(-1, 0) in directions:
            global s0
            s0 = 1
        if Vector2D(1, 0) in directions:
            global s1
            s1 = 1
        if Vector2D(0, -1) in directions:
            global s2
            s2 = 1
        if Vector2D(0, 1) in directions:
            global s3
            s3 = 1
        #labels for directions
        avail_dirs = {(-1, 0):1, (1, 0):2, (0, -1):3, (0, 1):4}
        g = self.nearest_ghost()
        #if nearest ghost exists(distance lesser than some specified value)
        if g:
            global s4
            dmax = 64
            index = 0
            for i in range(len(self.pacman.currentnode.neighbors)):
                n = self.pacman.currentnode.neighbors[i]
                mdist = Vector2D.magnitude(n.position-g.pos)
                if (mdist >= dmax):
                    index = i
                    dmax = mdist
            preferred_direction = self.pacman.currentnode.directions[index]
            s4 = avail_dirs[(preferred_direction.x, preferred_direction.y)]
        else:
            c = self.nearest_coin()
            coinVector = Vector2D(c.pos[0], c.pos[1])
            global s4
            dmin = Vector2D.magnitude(self.pacman.pos - coinVector)
            index = 0
            for i in range(len(self.pacman.currentnode.neighbors)):
                n = self.pacman.currentnode.neighbors[i]
                mdist = Vector2D.magnitude(n.position-coinVector)
                if (mdist <= dmin):
                    index = i
                    dmin = mdist
            preferred_direction = self.pacman.currentnode.directions[index]

            s4 = avail_dirs[(preferred_direction.x, preferred_direction.y)]
        #following block to see from which direction ghost approaches
        for g in self.ghosts:
            if Vector2D(-1, 0).dotpro(g.direction) == -1 and \
                            (self.pacman.currentnode.position-g.currentnode.position).normalize().dotpro(g.direction) == 1:
                global s5
                s5 = 1
            if Vector2D(1, 0).dotpro(g.direction) == -1 and \
                            (self.pacman.currentnode.position-g.currentnode.position).normalize().dotpro(g.direction) == 1:
                global s6
                s6 = 1
            if Vector2D(0, -1).dotpro(g.direction) == -1 and \
                            (self.pacman.currentnode.position-g.currentnode.position).normalize().dotpro(g.direction) == 1:
                global s7
                s7 = 1
            if Vector2D(0, 1).dotpro(g.direction) == -1 and \
                            (self.pacman.currentnode.position-g.currentnode.position).normalize().dotpro(g.direction) == 1:
                global s8
                s8 = 1

        traplist = []
        if Vector2D(-1, 0) in directions:
            global s5
            traplist.append(s5)
        if Vector2D(1, 0) in directions:
            global s6
            traplist.append(s6)
        if Vector2D(0, -1) in directions:
            global s7
            traplist.append(s7)
        if Vector2D(0, 1) in directions:
            traplist.append(s8)

        if len(traplist) == sum(traplist):
            global s9
            s9 = 1

        key = [str(s0), str(s1), str(s2), str(s3), str(s4), str(s5), str(s6), str(s7), str(s8), str(s9)]
        return ''.join(key)
#--------------------------------------------------------------------------
    def add_key(self, k):
        dict = {}
        for direction in self.pacman.currentnode.directions:
            n = random()
            dict[(int(direction.x), int(direction.y))] = n
        self.qdictionary[k] = dict

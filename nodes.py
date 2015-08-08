__author__ = 'starlord'
from vectors import Vector2D

class Node(object):
    def __init__(self, pos, width, height):
        self.x, self.y = (pos)
        #self.coord = (self.x*width*1.0, self.y*height*1.0)
        self.position = Vector2D(self.x*width, self.y*height)
        self.neighbors = []
        self.target = None
        self.directions = []

    def validDirections(self):
        for node in self.neighbors:
            tempvec = node.position - self.position
            self.directions.append(tempvec.normalize())
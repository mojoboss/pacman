__author__ = 'starlord'
from vectors import Vector2D

class Node(object):
    def __init__(self, pos, width, height):
        self.col, self.row = (pos)
        self.position = Vector2D(self.col*width, self.row*height)
        self.neighbors = []
        self.target = None
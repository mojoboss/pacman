__author__ = 'starlord'
import numpy
from tiles import  Tile
class Tilegroup(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tilelist = []

    def createTileList(self, filename):
        layout = numpy.loadtxt(filename, dtype=str)
        col, row = layout.shape
        for i in range(row):
            for j in range(col):
                value = layout[j][i]
                if (value == '0'):
                    pos = (i*self.width, j*self.height)
                    self.tilelist.append(Tile((self.width, self.height), pos))
        return self.tilelist


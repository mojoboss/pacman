__author__ = 'starlord'
import numpy
from coins import Coin
class Coingroup(object):
    def __init__(self, radius):
        self.radius = radius
        self.coinlist = []

    def createCoinList(self, filename):
        layout = numpy.loadtxt(filename, dtype=str)
        col, row = layout.shape
        for i in range(row):
            for j in range(col):
                value = layout[j][i]
                if (value == 'X'):
                    pos = (i*self.radius, j*self.radius)
                    self.coinlist.append(Coin(self.radius, pos))
        return self.coinlist

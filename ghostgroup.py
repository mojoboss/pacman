__author__ = 'starlord'
import numpy
from ghost import Ghost
class Ghostgroup:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ghostlist = []

    def create_ghostlist(self, layoutfile, ghostfile, nodes):
        layout = numpy.loadtxt(layoutfile, dtype=str)
        ghost = numpy.loadtxt(ghostfile, dtype=str)
        col, row = layout.shape
        for i in range(row):
            for j in range(col):
                valuel = layout[j][i]
                valueg = ghost[j][i]
                if (valuel == '+' and valueg == 'G'):
                    node = self.initial_node(nodes, i, j)
                    self.ghostlist.append(Ghost(3.2, node, (255, 0, 0), (self.width, self.height),
                                                [node.position.x, node.position.y]))

        return self.ghostlist

    def initial_node(self, nodes, i, j):
        for n in nodes:
            if (n.x == i and n.y == j):
                return n
__author__ = 'starlord'
import numpy
from nodes import Node
class NodeGroup(object):
    def __init__(self, width, height):
        self.nodelist = []
        self.width = width
        self.height = height

    def getNode(self, row, col):
        '''Input a list of nodes, and the row and col integers.  Returns
        the Node object located at that grid position.'''
        for node in self.nodelist:
            if node.row == row and node.col == col:
                return node
        return None

    def createNodeList(self, filename):
        '''Create the list of nodes from a text file'''
        layout = numpy.loadtxt(filename, dtype = str)
        rows, cols = layout.shape
        for row in range(rows):
            for col in range(cols):
                if layout[row][col] == '+':
                    self.nodelist.append(Node((col,row), self.width,
                                              self.height))

        #remaining part to include neighbours
        for i in range(len(self.nodelist)):
            node = self.nodelist[i]
            dirs = ['Up', 'Down', 'Left', 'Right']
            for j in dirs:
                pos = self.find_neighbors_pos(node, j, layout)
                if pos:
                    self.nodelist[i].neighbors.append(self.find_node_from_pos(self.nodelist, pos))

        return self.nodelist
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#method to find the pos of the neighbor in a given direction
    def find_neighbors_pos(self, node, direction, layout):
        x, y = node.row, node.col
        if (direction == 'Right'):
            while True:
                try:
                    x += 1
                    char = layout[x][y]
                    if (char == '-'):
                        pass
                    elif (char == '+'):
                        return x, y
                    elif (char == '0'):
                        return None
                except IndexError:
                    return None
        elif (direction == 'Left'):
            while True:
                try:
                    x -= 1
                    char = layout[x][y]
                    if (char == '-'):
                        pass
                    elif (char == '+'):
                        return x, y
                    elif (char == '0'):
                        return None
                except IndexError:
                    return None
        elif (direction == 'Down'):
            while True:
                try:
                    y += 1
                    char = layout[x][y]
                    if (char == '-'):
                        pass
                    elif (char == '+'):
                        return x, y
                    elif (char == '0'):
                        return None
                except IndexError:
                    return None
        elif (direction == 'Up'):
            while True:
                try:
                    y -= 1
                    char = layout[x][y]
                    if (char == '-'):
                        pass
                    elif (char == '+'):
                        return x, y
                    elif (char == '0'):
                        return None
                except IndexError:
                    return None
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#method to return a node while the position is given
    def find_node_from_pos(self, nodelist, pos):
        x, y = pos
        for n in nodelist:
            if n.row==x and n.col==y:
                return n
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
__author__ = 'starlord'
class Stack(object):
    def __init__(self):
        self.items = []

    def clear(self):
        '''Empties out a stack'''
        self.items = []

    def peek(self):
        '''Return the data at the top of the stack'''
        if len(self.items) > 0:
            return self.items[len(self.items)-1]
        return None

    def push(self, item):
        '''Put the incoming data at the top of the stack'''
        self.items.append(item)

    def pop(self):
        '''Remove the data at the top of the stack'''
        if len(self.items) > 0:
            removedItem = self.items.pop(len(self.items)-1)
            return removedItem
        return None
__author__ = 'starlord'
import Queue
#this method runs bfs on nodes graph and returns a python map of the form
#'map[child] = parent'
def search_pacnode(ghostnode, pacnode):
    q = Queue.Queue()
    q.put(ghostnode)
    map = {}
    explored = []
    while not q.empty():
        node = q.get()
        explored.append(node)
        if(node == pacnode):
            return map
        else:
            for n in node.neighbors:
                if n not in explored:
                    q.put(n)
                    map[n] = node


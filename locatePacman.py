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

def search_pacnode_dfs(ghostnode, pacnode):
    q = []
    q.append(ghostnode)
    map = {}
    explored = []
    while len(q)>0:
        node = q.pop()
        explored.append(node)
        if(node == pacnode):
            return map
        else:
            for n in node.neighbors:
                if n not in explored:
                    q.append(n)
                    map[n] = node

def search_pacnode_by_alg(ghostnode, pacnode, alg):
    if alg == 'dfs':
        return search_pacnode_dfs(ghostnode, pacnode)
    elif alg == 'bfs':
        return search_pacnode(ghostnode, pacnode)

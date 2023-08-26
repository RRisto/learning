# SISO program shortestPath.py

# Solves the computational problem ShortestPath. The algorithm
# employed is Bellman-Ford. It is in O(numVertices * numEdges), hence
# certainly O(n^2), where n is the length of the string input.

# inString: consists of a weighted, undirected graph G (in the ASCII
# format described in the textbook) followed by source vertex v and
# destination vertex w. G, v, and w are separated by semicolons and
# optional whitespace.

# returns: The length of the shortest path from v to w in G, or 'no'
# if there is no such path.

# Example:
# >>> shortestPath('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2 ; a; d')
# '7'
import utils; from utils import rf
from graph import Graph, Path, Edge

def shortestPath(inString):
    graphStr, source, dest = [x.strip() for x in inString.split(';')]
    graph = Graph(graphStr, weighted=True, directed=False)
    assert source in graph
    assert dest in graph

    # Bellman-Ford works on directed graphs.
    graph.convertToDirected()
    # This will give us the shortest path lengths to every vertex, and
    # the paths themselves.
    shortest, pred = bellmanFord(graph, source)
    # Of course we only wanted the distance to the destination, so
    # that is what we return.
    dist = shortest[dest]
    if dist == utils.inf:
        return 'no'
    else:
        return str( shortest[dest] )

# copied from page 86 of Cormen, Algorithms Unlocked. See that book
# for detailed documentation.
def relax(u,v,weight,shortest,pred):
    newDist = shortest[u] + weight
    if newDist < shortest[v]:
        shortest[v] = newDist
        pred[v] = u

# copied from page 102 of Cormen, Algorithms Unlocked. See that book
# for detailed documentation.
def bellmanFord(G,s):
    shortest = dict()
    pred = dict()
    for v in G:
        shortest[v] = utils.inf
        pred[v] = None
    shortest[s] = 0
    edges = G.getEdgesAsDict()
    for i in range(len(G)-1):
        for edge, weight in edges.items():
            u = edge.start()
            v = edge.end()
            relax(u,v,weight,shortest,pred)
    return shortest, pred
                    
def testShortestPath():
    testvals = [
        ('a,b,5 ; a; b', 5),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2 ; a; b', 5),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2 ; a; c', 1),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2 ; a; d', 7),
        ('a,b,5 b,c,6 d,a,9 a,c,1 d,b,2 ; a; b', 5),
        ('a,b,5 b,c,6 d,a,9 a,c,1 ; a; b', 5),
        ('a,b,1 b,c,1 c,d,1 d,e,1 ; a; d', 3),
        ('a,b,1 b,c,1 c,d,1 d,e,1 a,e,5; a; e', 4),
        ('a,b,1 b,c,1 c,d,1 d,e,1 a,e,5 a,c,1; a; e', 3),
        ('a,b,5 c,d,7 ; a; c', 'no'),
    ]
    for (inString, solution) in testvals:
        val = shortestPath(inString)
        utils.tprint(inString, ':', val)
        assert val == str(solution)


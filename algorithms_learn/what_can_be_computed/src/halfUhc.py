# SISO program halfUhc.py

# Solves the computational problem halfUHC. Given an input which is a
# string representing an unweighted, undirected graph, it searches for a
# cycle that visits at least half of the nodes and returns one if it exists.

# inString: g where g is a string representation of an
# unweighted, undirected graph (see graph.py).

# returns: If a half Hamilton cycle exists in g, it is returned
# formatted as a sequence of node names separated by commas. If no
# such cycle exists, 'no' is returned.

# Example:
# >>> halfUhc('a,b b,c c,a a,d d,b')
# 'a,b,c'
import utils; from utils import rf
from graph import Graph, Edge, Path
from tspDirK import tspDirK
def halfUhc(inString):
    graph = Graph(inString, weighted = False, directed = False)
    # K is the smallest integer that is at least half the number of
    # nodes.
    K = int( (len(graph)+1)/2 )

    ##################################################################
    # If there are two or three vertices, our conversion won't work
    # correctly, so treat this as a special case.  In this special case,
    # a self edge produces a half-ham-cycle.
    if len(graph)==2 or len(graph)==3:
        for node in graph:
            if graph.containsEdge( Edge([node, node]) ): # that's a self edge
                return node
    if len(graph)==2:
        return 'no'
    ##################################################################

    # a cheap hack that happens to make the case of three and four nodes
    # work correctly
    if len(graph)==3 or len(graph)==4:
        K=3
        
    # Convert to an equivalent weighted, directed graph.
    newGraph = graph.clone()
    newGraph.convertToWeighted()
    newGraph.convertToDirected()
    
    cycle = tspDirK(str(newGraph) + ';' + str(K))
    return cycle

def testHalfUhc():
    testvals = [('', 'yes'),
                 ('a,b', 'no'),
                 ('a,a', 'yes'),
                 ('a,b b,c', 'no'),
                 ('a,b b,c c,a', 'yes'),
                 ('a,b b,c c,a d,e d,f', 'yes'),
                 ('a,b b,c c,a d,e f,g', 'no'),
                 ('a,b b,c c,a a,d', 'yes'),
                 ('a,b b,c c,a a,d b,d', 'yes'),
                 ('a,b b,c c,d d,e e,f f,g g,h h,i i,j h,a', 'yes'),
                 ('a,b b,c c,d d,e e,f f,g g,h h,i i,j d,a', 'no'),
                 ]
    for (inString, solution) in testvals:
        val = halfUhc(inString)
        utils.tprint(inString, ':', val)
        if solution=='no':
            assert val == solution
        else:
            g = Graph(inString, weighted=False, directed=False)
            path = Path.fromString(val)
            assert g.isCycle(path)
            assert g.cycleLength(path) >= len(g) / 2


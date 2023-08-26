# SISO program tspPath.py

# Solves the computational problem TSPPath. Given an input which is a
# string representing a weighted, undirected graph together with a
# source node and destination node, it searches for a shortest
# Hamilton path from source to destination and returns one if it
# exists.

# inString: a string representation of a weighted, undirected graph g
# (see graph.py), followed by the source and destination nodes
# separated by semicolons

# returns: If a Hamilton path from source to dest exists in g, a
# shortest such path is returned formatted as a sequence of node names
# separated by commas. If no such path exists, 'no' is returned.

# Example:
# >>> tspPath('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2 ; a ; b')
# 'a,c,d,b'
import utils; from utils import rf
from graph import Graph, Path, Edge
from tsp import tsp

def tspPath(inString):
    graphStr, source, dest = [x.strip() for x in inString.split(";")]
    graph = Graph(graphStr, weighted=True, directed=False)

    # If there are two vertices, our conversion won't work correctly,
    # so treat this as a special case.
    if len(graph)==2:
        if graph.containsEdge(Edge([source, dest])):
            return str(Path([source, dest]))
        else:
            return 'no'

    # add an overwhelmingly negative edge from source to dest, thus
    # forcing that to be part of a shortest Ham cycle.
    sumOfWeights = graph.sumEdgeWeights()
    fakeEdge = Edge([source, dest])
    graph.removeEdge(fakeEdge)
    graph.addEdge(fakeEdge, -sumOfWeights)
    tspSoln = tsp(str(graph))
    # print('graph', graph)
    # print('tspSoln', tspSoln)
    if tspSoln == 'no':
        return 'no'

    # convert from string to Path object
    tspSoln = Path.fromString(tspSoln)

    rotatedSoln = tspSoln.rotateToFront(source)
    if rotatedSoln[-1] != dest:
        # Probably oriented the wrong way (or else fakeEdge wasn't
        # used -- see below). Reverse then rotate source to front
        # again
        rotatedSoln = rotatedSoln.reverse().rotateToFront(source)

    # If dest still isn't at the end of the cycle, then the orginal graph didn't
    # have a Ham path from source to dest (but it did have a Ham
    # cycle -- a cycle that did *not* include fakeEdge).
    if  rotatedSoln[-1] != dest:
        return 'no'
    else:
        return str(rotatedSoln)

def testTspPath():
    testvals = [
        ('a,b,5;a;b', 5),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2;a;b', 11),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2 c,e,10 d,e,20;a;b', 33),
        ('a,b,5 b,c,6 d,a,9 a,c,1 d,b,2;a;b', 'no'),
        ('a,b,5 b,c,6 d,a,9 a,c,1;a;b', 'no'),
    ]
    for (inString, solution) in testvals:
        val = tspPath(inString)
        utils.tprint(inString.strip(), ':', val)
        if solution == 'no':
            assert val == solution
        else:
            graphStr, source, dest = [x.strip() for x in inString.split(";")]
            graph = Graph(graphStr, directed=False)
            path = Path.fromString(val)
            dist = graph.pathLength(path)
            assert graph.isHamiltonPath(path)
            assert dist == solution


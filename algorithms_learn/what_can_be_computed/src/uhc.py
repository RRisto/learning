# SISO program uhc.py

# Solves the computational problem UHC. Given an input which is a
# string representing an unweighted, undirected graph, it searches for a
# Hamilton cycle and returns one if it exists.

# inString: g where g is a string representation of an
# unweighted, undirected graph (see graph.py).

# returns: If a Hamilton cycle exists in g, it is returned
# formatted as a sequence of node names separated by commas. If no
# such cycle exists, 'no' is returned.

# Example:
# >>> uhc('a,b b,c c,a a,d d,b')
# 'a,c,b,d'
import utils; from utils import rf
from tsp import tsp
from graph import Graph, Edge, Path

def uhc(inString):
    graph = Graph(inString, weighted = False, directed = False)
    # If there are two vertices, our conversion won't work correctly,
    # so treat this as a special case.
    if len(graph)==2:
        return 'no'
    # Convert to an equivalent weighted graph.
    graph.convertToWeighted()
    newGraphString = str(graph)
    cycle = tsp(newGraphString)
    return cycle

def testUhc():
    testVals = [
        ('', True),
        ('a,b', False),
        ('a,b b,c', False),
        ('a,b b,c c,a', True),
        ('a,b b,c c,a a,d', False),
        ('a,b b,c c,a a,d b,d', True),
        ('aB,aA aB,aC aA,aC', True),
    ]
    for (inString, hasUhc) in testVals:
        result = uhc(inString)
        utils.tprint(inString, ':', result)
        if not hasUhc:
            assert result == 'no'
        else:
            g = Graph(inString, weighted=False, directed=False)
            path = Path.fromString(result)
            assert g.isHamiltonCycle(path)


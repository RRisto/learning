# SISO program dhc.py

# Solves the computational problem DHC. Given an input which is a
# string representing an unweighted, directed graph, it searches for a
# directed Hamilton circuit and returns one if it exists.

# inString: g where g is a string representation of an
# unweighted, directed graph (see graph.py).

# returns: If a directed Hamilton circuit exists in g, it is returned
# formatted as a sequence of node names separated by commas. If no
# such circuit exists, 'no' is returned.

# Example:
# >>> dhc('a,b b,c c,a a,d d,b')
# 'a,d,b,c'
import utils; from utils import rf
from tspDir import tspDir
from graph import Graph, Edge, Path

def dhc(inString):
    graph = Graph(inString, weighted = False, directed = True)
    # Convert to an equivalent weighted graph.
    graph.convertToWeighted()
    newGraphString = str(graph)
    cycle = tspDir(newGraphString)
    return cycle

def testDhc():
    testVals = [
        ('', True),
        ('a,b', False),
        ('a,b b,a', True),
        ('a,b b,c', False),
        ('a,b b,c c,a', True),
        ('a,b b,c c,a a,d', False),
        ('a,b b,c c,a a,d b,d', False),
        ('a,b b,c c,a a,d d,b', True),
    ]
    for (inString, hasDhc) in testVals:
        result = dhc(inString)
        utils.tprint(inString, ':', result)
        if not hasDhc:
            assert result == 'no'
        else:
            g = Graph(inString, weighted=False, directed=True)
            path = Path.fromString(result)
            assert g.isHamiltonCycle(path)


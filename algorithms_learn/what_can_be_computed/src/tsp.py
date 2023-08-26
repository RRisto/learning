# SISO program tsp.py

# Solves the computational problem TSP. Given an input which is a
# string representing a weighted, undirected graph, it searches for a
# shortest Hamilton cycle and returns one if it exists.

# inString: g where g is a string representation of a weighted,
# undirected graph (see graph.py).

# returns: If a Hamilton cycle exists in g, a shortest such cycle is
# returned formatted as a sequence of node names separated by
# commas. If no Hamilton cycle exists, 'no' is returned.

# Example:
# >>> tsp('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2')
# 'a,b,d,c'
import utils; from utils import rf
from graph import Graph, Edge, Path
from tspDir import tspDir
def tsp(inString):
    graph = Graph(inString, weighted=True, directed=False)
    # If there are two vertices, our conversion won't work correctly, so treat this as a special case.
    if len(graph)==2:
        return 'no'
    # Create an equivalent weighted directed graph.
    equivalentGraph = graph.clone()
    equivalentGraph.convertToWeighted()
    equivalentGraph.convertToDirected()

    cycle = tspDir(str(equivalentGraph))
    return cycle

def testTsp():
    testvals = [
        ('a,b,5', 'no', None),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2', 'a,b,d,c', 16),
        ('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,200', 'a,b,c,d', 28),
        ('a,b,5 b,c,6 d,a,9 a,c,1', 'no', None),
    ]
    for (inString, solution, length) in testvals:
        val = tsp(inString)
        utils.tprint(inString, ':', val)
        if solution == 'no':
            assert val == solution
        else:
            g = Graph(inString, weighted=True, directed=False)
            p = Path.fromString(val)
            assert g.isHamiltonCycle(p)
            assert g.cycleLength(p) == length


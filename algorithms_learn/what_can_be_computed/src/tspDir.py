# SISO program tspDir.py

# Solves the *directed* version of the computational problem
# TSP. Given an input which is a string representing a weighted,
# directed graph, it searches for a shortest Hamilton cycle and
# returns one if it exists.

# inString: g where g is a string representation of a weighted,
# directed graph (see graph.py).

# returns: If a Hamilton cycle exists in g, a shortest such cycle is
# returned formatted as a sequence of node names separated by
# commas. If no Hamilton cycle exists, 'no' is returned.

# Example:
# >>> tspDir('a,b,5 b,c,6 c,d,8 d,a,9 a,c,1 d,b,2')
# 'a,b,c,d'
import utils; from utils import rf
from graph import Graph, Edge, Path
from utils import WcbcException

def tspDir(inString):
    graph = Graph(inString)
    firstNode = graph.chooseNode()
    if firstNode == None: # graph contains no vertices
        return '' # this is a positive instance -- we return the empty cycle
    (cycle, distance) = shortestCycleWithPrefix(graph, Path([firstNode]), 0)
    if cycle != None:
        return str(cycle)
    else:
        return 'no'

# Find the shortest Hamilton cycle in the given graph that extends the
# given prefix. Parameter graph is a Graph object, parameter prefix is
# a list of nodes that form a path in the graph, and prefixDistance is
# the length of that path. Return value is a 2-tuple consisting of the
# Hamilton cycle found together with its total distance, or (None,
# None) if no such cycle exists.
def shortestCycleWithPrefix(graph, prefix, prefixDistance):
    if len(prefix) < len(graph):
        # At least one more node must be added to the path. For each
        # node N that can be reached from the final node of prefix, if N
        # is not already in prefix, append N to prefix and call
        # shortestCycleWithPrefix() recursively.
        return tryAllPrefixExtensions(graph, prefix, prefixDistance)
    else:
        # Recursion has bottomed out -- the prefix path already includes
        # every node, so we complete the cycle back to the first node,
        # and return it (or return None if there is no edge back to the
        # first node)
        return completeCycle(graph, prefix, prefixDistance)

# The parameters are exactly as for shortestCycleWithPrefix()
# above. If this path can be completed into a cycle via a single edge
# from last to first node, the cycle and its weight are returned as a
# 2-tuple, otherwise (None, None) is returned.
def completeCycle(graph, prefix, prefixDistance):
    firstNode = prefix.start()
    lastNode = prefix.end()
    edgeCompletingCycle = Edge([lastNode, firstNode])
    if not graph.containsEdge( edgeCompletingCycle ):
        return (None, None)
    else:
        cycleDistance = prefixDistance + graph.getWeight(edgeCompletingCycle)
        return (prefix, cycleDistance)

# See shortestCycleWithPrefix() for documentation. The only difference
# is that tryAllPrefixExtensions() is invoked with a guarantee that
# the given path, prefix, does not yet consist of all nodes so we must
# try to extend it.
def tryAllPrefixExtensions(graph, prefix, prefixDistance):
    if len(graph) == len(prefix):
        raise WcbcException('tryAllPrefixExtensions() received a path that includes every node')
    lastNode = prefix.end()
    bestCycle = None
    bestDistance = None
    for nextNode in graph.neighbors(lastNode):
        if nextNode not in prefix:
            extendedPrefix = prefix.extend(nextNode)
            extendedPrefixDistance = prefixDistance + graph.getWeight( Edge([lastNode, nextNode]) )
            (cycle, distance) = shortestCycleWithPrefix(graph, extendedPrefix, extendedPrefixDistance)
            if cycle != None:
                if bestDistance == None or distance < bestDistance:
                    bestDistance = distance
                    bestCycle = cycle
    return (bestCycle, bestDistance)

def testShortestCycleWithPrefix():
    graph = Graph('''
              a,b,5 b,a,3 b,c,6
              c,a,7 c,d,8 d,a,9 a,c,1 d,b,2
                      ''', directed = True)
    path = Path(['a'])
    val = shortestCycleWithPrefix(graph, path, 0)
    cycle, dist = val
    utils.tprint(val)
    assert graph.isHamiltonCycle(cycle)
    assert dist == 14

def testTspDir():
    testvals = [
        ('aC,aB,1 aA,aB,1 aC,aA,1 aB,aA,1 aB,aC,1 aA,aC,1', 3),
        ('', 0),
        ('a,a,3', 3),
        ('a,b,4', 'no'),
        ('a,b,4 b,a,9', 13),
        ('a,b,4 b,a,9 b,c,6 c,a,10', 20),
        ('a,b,4 b,a,9 b,c,6 c,a,10 a,c,2 c,b,3', 14),
        ('a,b,4 b,a,9 b,c,6 c,a,10 a,c,2 c,b,300', 20),
        ('a,b,4 b,a,9 b,c,6 c,a,10 a,c,2 c,b,3 c,d,1', 'no'),
    ]
    for (inString, solution) in testvals:
        val = tspDir(inString)
        utils.tprint(inString.strip(), ':', val)
        if solution == 'no':
            assert val == solution
        else:
            graph = Graph(inString, directed=True)
            cycle = Path.fromString(val)
            dist = graph.cycleLength(cycle)
            assert graph.isHamiltonCycle(cycle)
            assert dist == solution


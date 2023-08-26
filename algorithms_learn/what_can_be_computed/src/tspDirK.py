# SISO program tspDirK.py

# Solves a variant of TSP: we seek a directed shortest cycle that
# incorporates at least K nodes. That is, given an input which is a
# string representing (i) a weighted, directed graph and (ii) an
# integer K, tspDir searches for a shortest directed cycle containing
# at least K nodes and returns one if it exists.

# inString: g where g is a string representation of a weighted,
# directed graph (see graph.py), followed by a semicolon, followed by
# K.

# returns: If a directed cycle containing at least K nodes exists in
# g, a shortest such cycle is returned formatted as a sequence of node
# names separated by commas. If no such cycle exists, 'no' is
# returned.

# Example:
# >>> tspDirK('a,b,4 b,a,9 b,c,6 c,a,10;3')
# 'a,b,c'
import utils; from utils import rf
from graph import Graph, Edge, Path
from tspDir import completeCycle

# Variant of TSP. We seek a directed shortest cycle that incorporates
# at least K nodes. See tspDir.py for more detailed comments.
def tspDirK(inString):
    (graphString, K) = inString.split(';')
    K = int(K)
    # treat K=0 as a special case. Since the empty cycle satisfies
    # this, we return a positive solution which is the empty string.
    if K==0:
        return ''

    graph = Graph(graphString)
    bestCycle = None; bestDistance = None
    for firstNode in graph:
        (cycle, distance) = shortestKCycleWithPrefix(graph, K, Path([firstNode]), 0)
        if cycle != None:
            if bestDistance == None or distance < bestDistance:
                (bestCycle, bestDistance) = (cycle, distance)
    if bestCycle != None:
        return str(bestCycle)
    else:
        return 'no'

# See tspDir.py for documentation on shortestCycleWithPrefix, which is
# analogous to this function except we permit cycles to have K or more
# nodes.
def shortestKCycleWithPrefix(graph, K, prefix, prefixDistance):
    if len(prefix) >= K:
        (cycle1, distance1) = completeCycle(graph, prefix, prefixDistance)
    else:
        (cycle1, distance1) = (None, None)
    
    (cycle2, distance2) = tryAllKPrefixExtensions(graph, K, prefix, prefixDistance)
    if cycle1 == None and cycle2 == None:
        return (None, None)
    elif cycle1 == None and cycle2 != None:
        return (cycle2, distance2)
    elif cycle1 != None and cycle2 == None:
        return (cycle1, distance1)
    elif distance1 <= distance2:
        return (cycle1, distance1)
    else:
        return (cycle2, distance2)

# See tspDir.py for documentation on tryAllPrefixExtensions, which is
# analogous to this function except we permit cycles to have K or more
# nodes.
def tryAllKPrefixExtensions(graph, K, prefix, prefixDistance):
    if len(graph) == len(prefix):
        return (None, None)

    lastNode = prefix.end()
    bestCycle = None
    bestDistance = None
    for nextNode in graph.neighbors(lastNode):
        if nextNode not in prefix:
            extendedPrefix = prefix.extend(nextNode)
            extendedPrefixDistance = prefixDistance + graph.getWeight( Edge([lastNode, nextNode]) )
            (cycle, distance) = shortestKCycleWithPrefix(graph, K, extendedPrefix, extendedPrefixDistance)
            if cycle != None:
                if bestDistance == None or distance < bestDistance:
                    bestDistance = distance
                    bestCycle = cycle
    return (bestCycle, bestDistance)

def testTspDirK():
    testvals = [
        (';1', 'no'),
        ('a,a,3;1', 3),
        ('a,a,3 ; 1 ', 3),
        ('a,a,3;2', 'no'),
        ('a,b,4;1', 'no'),
        ('a,b,4;2', 'no'),
        ('a,b,4;3', 'no'),
        ('a,b,4 b,a,9;1', 13),
        ('a,b,4 b,a,9;2', 13),
        ('a,b,4 b,a,9;3', 'no'),
        ('a,b,4 b,a,9 b,c,6 c,a,10;2', 13),
        ('a,b,4 b,a,9 b,c,6 c,a,10;3', 20),
        ('a,b,4 b,a,9 b,c,6 c,a,1;2', 11),
        ('a,b,4 b,a,9 b,c,6 c,a,10;4', 'no'),
        ('a,b,4 b,a,9 b,c,6 c,a,10 a,c,2 c,b,3;3', 14),
        ('a,b,4 b,a,9 b,c,6 c,a,10 a,c,2 c,b,3;4', 'no'),
    ]
    for (inString, solution) in testvals:
        val = tspDirK(inString)
        utils.tprint(inString.strip(), ':', val)
        if solution == 'no':
            assert val == solution
        else:
            (graphString, K) = inString.split(';')
            graph = Graph(graphString, directed=True)
            K = int(K)
            cycle = Path.fromString(val)
            dist = graph.cycleLength(cycle)
            assert graph.isCycle(cycle)
            assert len(cycle) >= K
            assert dist == solution


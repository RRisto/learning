# SISO program clique.py

# Solves the computational problem Clique. Given an input in the form
# "graph ; K", it searches for a clique of size K and returns such a
# clique if it exists.

# inString: 'g ; K' where g is a string representation of an
# unweighted, undirected graph (see graph.py) and K is an integer.

# returns: If a clique of size K exists in g, it is returned formatted
# as a sequence of node names separated by commas. If no such clique
# exists, 'no' is returned.

# Example:
# >>> clique('a,b a,c a,d b,c b,d c,d c,e b,e d,e ; 4')
# 'd,e,b,c' [or another 4-clique]
import utils; from utils import rf
from graph import Graph, Edge
def clique(inString):
    (graphString, Kstring) = inString.split(';')
    G = Graph(graphString, weighted=False, directed=False)
    K = int(Kstring)

    # special case: if K=0, we have a positive solution but it's the empty string
    if K==0: return ''
    
    nodes = G.getNodesAsSet()
    emptyClique = set()
    clique = tryExtendClique(G, K, emptyClique, nodes)
    if clique:
        return ','.join(clique)
    else:
        return 'no'

# The parameter clique is a clique in the parameter graph, represented
# as a list of nodes. Return True if adding newNode produces a new
# clique, and otherwise return False.
def extendsClique(graph, clique, newNode):
    """Return True if adding newNode produces a new clique, and otherwise return False.

    Args:

        graph (Graph): a graph

        clique (set of str): a clique in the graph; each of the
            strings in the set should be the name of a node in the
            graph

        newNode (str): the name of a node in the graph

    Returns:

        bool: Return True if adding newNode to clique produces a new
           clique in graph, and otherwise return False.

    """
    
    for node in clique:
        if not graph.containsEdge( Edge([node, newNode]) ):
            return False
    return True

def testExtendsClique():
    G = 'a,b a,c a,d b,c b,d c,d c,e b,e d,e'
    G = Graph(G, weighted=False, directed=False)
    testvals = [
        ([], 'a', True),
        (['a'], 'b', True),
        (['a'], 'c', True),
        (['a', 'b'], 'c', True),
        (['a', 'b'], 'd', True),
        (['a', 'b', 'c'], 'd', True),
        (['a'], 'e', False),
        (['a', 'b'], 'e', False),
        (['a', 'b', 'c'], 'e', False),
    ]
    for (clique, newNode, solution) in testvals:
        val = extendsClique(G, clique, newNode)
        utils.tprint(clique, newNode, val)
        assert val == solution

def tryExtendClique(graph, K, clique, remainingNodes):
    """Attempt to extend the given clique to a clique of size K.

    If the given clique can be extended to a clique of size K by adding
    nodes from the remainingNodes, return such a clique. Otherwise,
    return None.

    Args:

        graph (Graph): a graph

        K (int): the size of the clique we are trying to create by
            extending the current clique

        clique (set of str): a clique in the graph; each of the
            strings in the set should be the name of a node in the
            graph

        remainingNodes (iterable of str): a list of nodes from which
            we can choose in order to extend the clique.

    Returns:

        set of str: If the clique could be extended, this set contains
            the node names of the extended clique. If it couldn't be
            extended, None is returned.

    """
    
    if len(clique) == K:
        return clique
    elif len(remainingNodes)==0:
        return None
    else:
        nextNode = next(iter(remainingNodes)) # pick a remaining element
        newRemainingNodes = remainingNodes - {nextNode}
        if extendsClique(graph, clique, nextNode):
            newClique = clique | {nextNode}
            extendedClique = tryExtendClique(graph, K, newClique, newRemainingNodes)
            if extendedClique:
                return extendedClique
        return tryExtendClique(graph, K, clique, newRemainingNodes)

def testTryExtendClique():
    G = 'a,b a,c a,d b,c b,d c,d c,e b,e d,e'
    G = Graph(G, weighted=False, directed=False)
    utils.tprint('Trying to extend cliques in', G)
    testvals = [
        (1, set({}), set({'a', 'b', 'c', 'd', 'e'}), 'verify'),
        (2, set({}), set({'a', 'b', 'c', 'd', 'e'}), 'verify'),
        (3, set({}), set({'a', 'b', 'c', 'd', 'e'}), 'verify'),
        (4, set({}), set({'a', 'b', 'c', 'd', 'e'}), 'verify'),
        (5, set({}), set({'a', 'b', 'c', 'd', 'e'}), None),
        (4, set({'c', 'd', 'e'}), set({'a', 'b'}), 'verify'),
        (5, set({'c', 'd', 'e'}), set({'a', 'b'}), None),
        (4, set({'a', 'c'}), set({'b', 'd', 'e'}), 'verify'),
        (5, set({'a', 'c'}), set({'b', 'd', 'e'}), None),
    ]
    for (K, clique, remainingNodes, solution) in testvals:
        val = tryExtendClique(G, K, clique, remainingNodes)
        utils.tprint(K, clique, remainingNodes, val)
        if solution is None:
            assert val == solution
        else: # need to verify the solution
            assert G.isClique(val)
            assert len(val) == K

    
def testClique():
    graphString = 'a,b a,c a,d b,c b,d c,d c,e b,e d,e'
    G = Graph(graphString, weighted=False, directed=False)
    testvals = [
        (1, 'verify'),
        (2, 'verify'),
        (3, 'verify'),
        (4, 'verify'),
        (5, None),
    ]
    for (K, solution) in testvals:
        inString = graphString + ' ; ' + str(K)
        val = clique(inString)
        utils.tprint(inString, val)
        if solution is None:
            assert val == 'no'
        else: # need to verify the solution
            nodes = val.split(',')
            assert G.isClique(nodes)
            assert len(nodes) == K



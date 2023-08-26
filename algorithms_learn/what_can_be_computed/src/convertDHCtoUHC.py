# SISO program convertDHCtoUHC.py

# Convert an instance of directed Hamilton cycle (DHC) into an
# equivalent instance of undirected Hamilton cycle (UHC).

# inString: an instance of DHC. This consists of a directed,
# unweighted graph. See the textbook or graph.py for details of
# representing a graph as a string.

# returns: an instance of UHC. This consists of an undirected,
# unweighted graph in string format. The instance is created via the
# "triplet" construction described in the textbook.

# Example:
# >>> convertDHCtoUHC('a,b b,c c,a')
# 'aA,aB aA,bC aB,aC aC,cA bA,bB bA,cC bB,bC cA,cB cB,cC'
import utils; from utils import rf
from graph import Graph, Edge

def convertDHCtoUHC(inString):
    # G is the original instance
    G = Graph(inString, weighted = False, directed = True)
    # newG is the converted instance -- create an empty graph using empty string
    newG = Graph('', weighted = False, directed = False)
    # Create all of the nodes of newG -- a triplet of A, B, and C
    # nodes in newG for every node in G.  Also create an A-B edge and
    # a B-C edge within each triplet.
    for node in G:
        # Create triplet.
        nodeA = node + 'A'
        nodeB = node + 'B'
        nodeC = node + 'C'
        newNodes = (nodeA, nodeB, nodeC)
        for newNode in newNodes:
            newG.addNode(newNode)
        # Create A-B and B-C edges within the triplet.
        newG.addEdge(Edge([nodeA, nodeB]))
        newG.addEdge(Edge([nodeB, nodeC]))
    # Create all the remaining edges of newG, i.e., create an undirected
    # A-C edge corresponding to each directed edge in G.
    for edge in G.edges():
        (node1, node2) = edge.nodes
        newEdge = Edge([node1 + 'A', node2 + 'C'])
        newG.addEdge( newEdge )

    return str(newG)

# need this for testing
def revertSolution(uhcSoln):
    if uhcSoln == 'no': 
        return 'no'
    uhcSolnNodes = uhcSoln.split(',')
    # extract every third element (i.e., one of each triplet)
    nodes = [uhcSolnNodes[i] for i in range(0,len(uhcSolnNodes),3)]
    # delete final character (the 'A', for A-child)
    nodes = [n[:-1] for n in nodes]
    return ','.join(nodes)
    
def testConvertDHCtoUHC():
    from uhc import uhc
    from dhc import dhc
    from graph import Path
    instances = [
                 '',
                 'a,a',
                 'a,b',
                 'a,b b,a',
                 'a,b b,c c,a',
                 'a,b b,c a,c',
                 'a,b b,c c,d',
                 'a,b b,c c,d d,a',
                 'a,b b,c c,d a,d',
                 'a,b b,c c,d a,d d,b c,a',
                ]
    for instance in instances:
        convertedInstance = convertDHCtoUHC(instance)
        instanceSolution = dhc(instance)
        convertedInstanceSolution = uhc(convertedInstance)
        revertedSolution = revertSolution(convertedInstanceSolution)

        utils.tprint(instance, 'maps to', convertedInstance,\
              ' solutions were: ', instanceSolution, ';', convertedInstanceSolution)
        utils.tprint('revertedSolution', revertedSolution)

        if revertedSolution=='no':
            assert instanceSolution=='no'
        else:
            g = Graph(instance, weighted=False)
            path = Path.fromString(revertedSolution)
            # print('g', g, 'path', path)
            assert g.isHamiltonCycle(path) or g.isHamiltonCycle(path.reverse())



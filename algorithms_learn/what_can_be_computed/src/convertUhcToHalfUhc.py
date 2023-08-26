# SISO program convertUhcToHalfUhc.py

# Convert an instance of undirected Hamilton cycle (UHC) into an
# equivalent instance of half UHC.

# inString: an instance of UHC. This consists of an undirected,
# unweighted graph. See the textbook or graph.py for details of
# representing a graph as a string.

# returns: an instance of half UHC. This consists of an undirected,
# unweighted graph in string format, which is essentially two copies
# of the original input.

# Example:
# >>> convertUhcToHalfUhc('a,b b,c c,a')
# 'aA,bA aA,cA aB,bB aB,cB bA,cA bB,cB'
import utils; from utils import rf
from graph import Graph, Edge

def convertUhcToHalfUhc(inString):
    # G is the original instance
    G = Graph(inString, weighted = False, directed = False)
    # newG is the converted instance -- create an empty graph using empty string
    newG = Graph('', weighted = False, directed = False)
    # Create all of the nodes of newG -- a pair of ``twin'' A-, and B-
    # nodes in newG for every node in G.
    for node in G:
        # Create twins.
        nodeA = node + 'A'
        nodeB = node + 'B'
        newNodes = (nodeA, nodeB)
        for newNode in newNodes:
            newG.addNode(newNode)
    # Create all the remaining edges of newG, i.e., create twin edges
    # corresponding to each edge in G.
    for edge in G.edges():
        node1, node2 = edge.nodes
        newG.addEdge( Edge( [node1 + 'A', node2 + 'A'] ) )
        newG.addEdge( Edge( [node1 + 'B', node2 + 'B'] ) )

    return str(newG)

# need this for testing. 
def revertSolution(halfUhcSoln):
    if halfUhcSoln == 'no': 
        return 'no'
    nodes = halfUhcSoln.split(',')
    # delete final character (the ``A'' or ``B'' that was added)
    nodes = [n[:-1] for n in nodes]
    return ','.join(nodes)

    
def testConvertUhcToHalfUhc():
    from uhc import uhc
    from halfUhc import halfUhc
    from graph import Path
    instances = [
                 '',
                 'a,a',
                 'a,b',
                 'a,b b,c c,a',
                 'a,b b,c c,d',
                 'a,b b,c c,d d,a',
                 'a,b b,c c,d a,d d,b c,a',
                ]
    for instance in instances:
        convertedInstance = convertUhcToHalfUhc(instance)
        instanceSolution = uhc(instance)
        convertedInstanceSolution = halfUhc(convertedInstance)
        revertedSolution = revertSolution(convertedInstanceSolution)

        utils.tprint(instance, 'maps to', convertedInstance,\
              ' solutions were: ', instanceSolution, ';', convertedInstanceSolution)
        utils.tprint('revertedSolution', revertedSolution)

        if revertedSolution=='no':
            assert instanceSolution=='no'
        else:
            g = Graph(instance, weighted=False, directed=False)
            path = Path.fromString(revertedSolution)
            # print('g', g, 'path', path)
            assert g.isHamiltonCycle(path)



    # instances = ['',
    #              'a,a',
    #              'a,b',
    #              'a,b b,a',
    #              'a,b b,c c,a',
    #              'a,b b,c a,c',
    #              'a,b b,c c,d',
    #              'a,b b,c c,d d,a',
    #              'a,b b,c c,d a,d',
    #              'a,b b,c c,d a,d d,b c,a',
    #             ]
    # for instance in instances:
    #     convertedInstance = convertUhcToHalfUhc(instance)
    #     instanceSolution = uhc(instance)
    #     convertedInstanceSolution = halfUhc(convertedInstance)
    #     print(instance, 'maps to', convertedInstance,\
    #           ' solutions were: ', instanceSolution, ';', convertedInstanceSolution)



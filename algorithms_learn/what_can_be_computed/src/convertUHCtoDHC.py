# SISO program convertUHCtoDHC.py

# Convert an instance of undirected Hamilton cycle (UHC) into an
# equivalent instance of directed Hamilton cycle (DHC).

# inString: an instance of UHC. This consists of an undirected,
# unweighted graph. See the textbook or graph.py for details of
# representing a graph as a string.

# returns: an instance of DHC. This consists of a directed, unweighted
# graph in string format. The instance is created via the construction
# described in the textbook, in which each undirected edge is replaced
# by two directed edges.

# Example:
# >>> convertUHCtoDHC('a,b b,c c,d d,a')
# 'a,b a,d b,a b,c c,b c,d d,a d,c'
import utils; from utils import rf
from graph import Graph, Edge

def convertUHCtoDHC(inString):
    # G is the original instance
    G = Graph(inString, weighted = False, directed = False)
    # newG is the converted instance -- create an empty graph using empty string
    newG = Graph('', weighted = False, directed = True)
    # add all nodes of G to newG
    for node in G:
        newG.addNode(node)

    undirectedEdges = G.getEdgesAsSet()
    # special case: single edge gets converted to single edge
    if len(undirectedEdges)==1:
        # extract the one and only edge using a for loop
        for theEdge in undirectedEdges:
            newG.addEdge(theEdge)
            return str(newG)

    # add all original edges and their reverse to the new graph
    for edge in undirectedEdges:
        # New edge is the reverse of the old one.
        newEdge = Edge( [edge[1], edge[0]] )
        # Add original and reversed edge to the new graph
        newG.addEdge(edge)
        newG.addEdge(newEdge)

    return str(newG)

# need this for testing. In fact, reverting the solution is trivial
# for this conversion.
def revertSolution(dhcSoln):
    return dhcSoln


    
def testConvertUHCtoDHC():
    from uhc import uhc
    from dhc import dhc
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
        convertedInstance = convertUHCtoDHC(instance)
        instanceSolution = uhc(instance)
        convertedInstanceSolution = dhc(convertedInstance)
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



    # instances = ['v1,v2 v2,v3 v3,v1 v2,v4 v1,v4', '', 'v1,v2', 'v1,v2 v1,v3']
    # for instance in instances:
    #     convertedInstance = convertUHCtoDHC(instance)
    #     instanceSolution = uhc(instance)
    #     convertedInstanceSolution = dhc(convertedInstance)
    #     print(instance, 'maps to', convertedInstance,\
    #           ' solutions were: ', instanceSolution, ';', convertedInstanceSolution)



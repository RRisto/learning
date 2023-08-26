# SISO program convertSatToClique.py

# Convert an instance of SAT into an
# equivalent instance of Clique.

# inString: an instance of SAT, formatted as described in the textbook
# and sat.py.

# returns: an instance of Clique, formatted as described in the textbook.

# Example:
# >>> convertSatToClique('x1 OR x2 AND NOT x1 OR NOT x2 AND x2')
# 'x1nC2,x2pC1 x1nC2,x2pC3 x1pC1,x2nC2 x1pC1,x2pC3 x2pC1,x2pC3;3'
import utils; from utils import rf
import sat
from graph import Graph, Edge
def convertSatToClique(inString):
    cnfFormula = sat.readSat(inString)
    numClauses = len(cnfFormula)
    graph = Graph('', weighted=False, directed=False)
    for clauseID in range(len(cnfFormula)):
        clause = cnfFormula[clauseID]
        # to correspond with textbook's notation, clause IDs start
        # from 1, not 0, so we need 'clauseID+1' here:
        clauseDescriptor = 'C' + str(clauseID+1)
        for variable, posOrNeg in clause.items():
            if posOrNeg == 1:
                graph.addNode(variable + 'p' + clauseDescriptor)
            elif posOrNeg == -1:
                graph.addNode(variable + 'n' + clauseDescriptor)
            else: # both pos and neg
                graph.addNode(variable + 'p' + clauseDescriptor)
                graph.addNode(variable + 'n' + clauseDescriptor)

    for node1 in graph:
        (literalName1, clauseID1) = node1.rsplit('C', 1)
        for node2 in graph:
            (literalName2, clauseID2) = node2.rsplit('C', 1)
            # no edge if in same clause
            if clauseID1 == clauseID2:
                continue
            # no edge if literals are negations of each other
            variableName1 = literalName1[:-1]
            posOrNeg1 = literalName1[-1]
            variableName2 = literalName2[:-1]
            posOrNeg2 = literalName2[-1]
            if variableName1==variableName2 and posOrNeg1 != posOrNeg2:
                continue
            # otherwise, need an edge between the nodes (but skip if
            # already added, which could have happened in the other
            # order since graph is undirected)
            e = Edge([node1, node2])
            if not graph.containsEdge(e):
                graph.addEdge( e )

    # Annoying special case: single node. Give it a single self-edge so
    # that it doesn't get represented as an empty graph when converted
    # to a string.
    ### not needed anymore?
    # if len(graph)==1:
    #     for node in graph:
    #         graph.addEdge( Edge([node, node]) )

    graphString = str(graph)
    k = str(numClauses)
    return graphString + ';' + k

# need this for testing
def revertSolution(cliqueSoln):
    if cliqueSoln == 'no': 
        return 'no'
    nodes = cliqueSoln.split(',') if cliqueSoln!='' else []
    # Remove everything after the 'C' in each node name
    nodes = [n[:n.index('C')] for n in nodes]
    # build truth assignment
    truthAssignment = dict()
    for node in nodes:
        variableName = node[:-1]
        posNeg = node[-1:]
        if posNeg=='p':
            truthAssignment[variableName] = True
        elif posNeg=='n':
            truthAssignment[variableName] = False
        else:
            raise utils.WcbcException('Unexpected node name' + node)

    return truthAssignment

def testConvertSatToClique():
    import sat
    from clique import clique
    for satInstance in ['',
                     'x1',
                     '(x1) AND (x2)',
                     '(x1) AND (NOT x2) AND (NOT x1)',
                     '(x1 OR x2) AND (NOT x2 OR x3 OR x1) AND (NOT x1)  AND (NOT x3 OR NOT x2)',
                        'x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3',
                        'x1 OR x2 AND NOT x1 OR NOT x2 AND x2',
                        'x1 OR NOT x1',
    ]:
        utils.tprint( 'satInstance:', satInstance )
        cliqueInstance = convertSatToClique(satInstance)
        utils.tprint( 'cliqueInstance:', cliqueInstance )
        satSolution = sat.sat(satInstance)
        cliqueSolution = clique(cliqueInstance)
        utils.tprint('satSolution:', satSolution)
        utils.tprint('cliqueSolution:', cliqueSolution)
        utils.tprint()
        if satSolution == 'no':
            assert cliqueSolution == 'no'
        else:
            truthAssignment = revertSolution(cliqueSolution)
            utils.tprint(truthAssignment)
            assert sat.satisfies(sat.readSat(satInstance), truthAssignment)
        


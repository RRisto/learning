# file graphTests.py

# Contains test functions for graph.py

import utils; from utils import rf
from graph import *


def testPathStr():
    testvals = [
        ([], ''),
        ([''], 'exception'),
        ('', 'exception'),
        ('asdf', 'exception'),
        ([1,2,3,4], 'exception'),
        (['a1'], 'a1'),
        (['ab1'], 'ab1'),
        (['ab1', 'zxy'], 'ab1,zxy'),
        ('a,b,c'.split(','), 'a,b,c'),
        ('a,b,,c'.split(','), 'exception'),
        ('a1,b1,c1'.split(','), 'a1,b1,c1'),
    ]
    for (nodes, solution) in testvals:
        try:
            p = Path(nodes)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception, as expected'
        utils.tprint(nodes,':',solution)
        s = str(p)
        if solution != 'exception':
            assert s == solution

def testPathReverse():
    testvals = [
        ([], Path([])),
        (['1'], Path(['1'])),
        (['a1'], Path(['a1'])),
        (['ab1'], Path(['ab1'])),
        (['ab1', 'zxy'], Path(['zxy', 'ab1'])),
        ('a,b,c'.split(','), Path('c,b,a'.split(','))),
        ('a1,b1,c1'.split(','), Path('c1,b1,a1'.split(','))),
    ]
    for (nodes, solution) in testvals:
        p = Path(nodes)
        val = p.reverse()
        utils.tprint(p,':',val)
        assert val == solution

def testPathExtend():
    testvals = [
        ([], 'x', Path(['x'])),
        ([], 'xyz', Path(['xyz'])),
        (['1'], 'x', Path(['1', 'x'])),        
        (['1'], 'xyz', Path(['1', 'xyz'])),
        (['a1'], 'x', Path(['a1', 'x'])),
        (['a1'], 'xyz', Path(['a1', 'xyz'])),
        (['ab1', 'zxy'], 'xyz', Path(['ab1', 'zxy', 'xyz'])),
        ('a,b,c'.split(','), 'xyz', Path('a,b,c,xyz'.split(','))),
        ('a1,b1,c1'.split(','), 'xyz', Path('a1,b1,c1,xyz'.split(','))),
    ]
    for (nodes, newNode, solution) in testvals:
        p = Path(nodes)
        val = p.extend(newNode)
        utils.tprint(p, ';', newNode, ':', val)
        assert val == solution

def testPathRotateToFront():
    testvals = [
        (['1'], '1', Path(['1'])),
        (['a1'], 'a1', Path(['a1'])),
        (['ab1', 'zxy'], 'zxy', Path(['zxy', 'ab1'])),
        (['ab1', 'zxy'], 'ab1', Path(['ab1', 'zxy'])),
        ('a,b,c'.split(','), 'a', Path('a,b,c'.split(','))),
        ('a,b,c'.split(','), 'b', Path('b,c,a'.split(','))),
        ('a,b,c'.split(','), 'c', Path('c,a,b'.split(','))),
        ('a,b,c'.split(','), 'd', 'exception'),
    ]
    for (nodes, node, solution) in testvals:
        p = Path(nodes)
        try:
            val = p.rotateToFront(node)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception, as expected'
        utils.tprint(p, ';', node, ':',val)
        if solution != 'exception':
            assert val == solution

def testPathEquals():
    p1 = Path([])
    p1b = Path([])
    p2 = Path(['a'])
    p2b = Path(['a'])
    p3 = Path(['a123'])
    p4 = Path(['a', 'b'])
    p5 = Path(['a123', 'b123'])
    p4r = Path(['b', 'a'])
    p5r = Path(['b123', 'a123'])
    p6 = Path(['a', 'b', 'c'])
    p6b = Path(['a', 'b', 'c'])
    p6r = Path(['c', 'b', 'a'])
    e4 = Edge(['a', 'b'])
    e5 = Edge(['a123', 'b123'])
    e4r = Edge(['b', 'a'])
    e5r = Edge(['b123', 'a123'])

    testvals = [
        (p1, p1, True),
        (p1, p1b, True),
        (p2, p2b, True),
        (p4, p4, True),
        (p4, p4r, False),
        (p5, p5r, False),
        (p6, p6b, True),
        (p6, p6r, False),
        (p4, p6, False),
        (p4, e4, True),
        (p5, e5, True),
        (p4, e4r, False),
        (p5r, e5, False),
        (None, p5, False),
        (p5, None, False),
        (p5, "asdf", False),
    ]
    for (path1, path2, solution) in testvals:
        val = (path1==path2)
        utils.tprint(path1, path2, ':', val)
        assert val == solution

def testPathContains():
    p1 = Path([])
    p2 = Path(['a'])
    p4 = Path(['a', 'b'])
    p6 = Path(['a', 'b', 'c'])
    e5 = Edge(['a123', 'b123'])

    testvals = [
        (p1, 'a', False),
        (p2, 'a', True),
        (p4, 'a', True),
        (p4, 'b', True),
        (p4, 'c', False),
        (e5, 'a123', True),
        (e5, 'b123', True),
        (e5, 'c123', False),
        (p6, 'a', True),
        (p6, 'b', True),
        (p6, 'c', True),
        (p6, 'd', False),
    ]
    for (path, node, solution) in testvals:
        val = (node in path)
        utils.tprint(path, node, ':', val)
        assert val == solution

def testPathIter():
    e_ab = Edge(['a', 'b'])
    e_bc = Edge(['b', 'c'])
    e_cd = Edge(['c', 'd'])
    e_ba = Edge(['b', 'a'])
    e_aa = Edge(['a', 'a'])
    e_bb = Edge(['b', 'b'])
    e_ca = Edge(['c', 'a'])
    p1 = Path([])
    p1Edges = []
    p2 = Path(['a'])
    p2Edges = []
    p3 = Path(['a', 'b'])
    p3Edges = [ e_ab ]
    p4 = Path(['a', 'b', 'c'])
    p4Edges = [ e_ab, e_bc ]
    p5 = Path(['a', 'b', 'c', 'd'])
    p5Edges = [ e_ab, e_bc, e_cd ]
    p6 = Path(['a', 'b', 'a'])
    p6Edges = [ e_ab, e_ba ]
    p6 = Path(['a', 'b', 'b'])
    p6Edges = [ e_ab, e_bb ]
    p7 = Path(['a', 'a'])
    p7Edges = [ e_aa ]
    p8 = Path(['a', 'b', 'c', 'a', 'b'])
    p8Edges = [ e_ab, e_bc, e_ca, e_ab ]


    testvals = [
        (p1, p1Edges),
        (p2, p2Edges),
        (p3, p3Edges),
        (p4, p4Edges),
        (p5, p5Edges),
        (p6, p6Edges),
        (p7, p7Edges),
        (p8, p8Edges),
    ]
    for (path, solution) in testvals:
        val = [e for e in path]
        utils.tprint(path, ':', val)
        assert val == solution

def testGraphStr():
    testvals = [( ('',), ''),
                ( ('', False), ''),
                ( ('', False, False), ''),
                ( ('a',), 'a'),
                ( ('a,a', False), 'a,a'),
                ( ('a,b', False), 'a,b'),
                ( ('a,b c', False), 'a,b c'),
                ( ('x,z x,y c', False), 'c x,y x,z'),
                ( ('x,z dd x x,y cc', False), 'cc dd x,y x,z'),
                ( ('a,a', False, False), 'a,a'),
                ( ('a,b', False, False), 'a,b'),
                ( ('b,a', False, False), 'a,b'),
                ( ('a,b,5',), 'a,b,5'),
                ( ('a11,a11', False), 'a11,a11'),
                ( ('a11,a11,9', ), 'a11,a11,9'),
                ( ('b,a a,a', False, False), 'a,a a,b'),
                ( ('b,a,3 a,a,4', True, False), 'a,a,4 a,b,3'),
                ( ('b,a,3 a,a,4',), 'a,a,4 b,a,3'),
                ( ('bb,a,3 a,a,4 a,ccc,5 bb,d,6', True, True), 'a,a,4 a,ccc,5 bb,a,3 bb,d,6'),
                ( ('bb,a,3 a,a,4 a,ccc,5 bb,d,6', True, False), 'a,a,4 a,bb,3 a,ccc,5 bb,d,6'),
                ( ('bb,a a,a a,ccc bb,d', False, True), 'a,a a,ccc bb,a bb,d'),
                ( ('bb,a a,a a,ccc bb,d', False, False), 'a,a a,bb a,ccc bb,d'),
                ( ('bb,a a,a a,ccc a,bb bb,d', False, False), 'exception'),
                ( ('bb,a a,a a,ccc bb,a bb,d', False, False), 'exception'),
                ( ('bb,a a,a a,ccc a,bb bb,d', False, True), 'a,a a,bb a,ccc bb,a bb,d'),
                ( ('bb,a a,a a,ccc bb,a bb,d', False, True), 'exception'),
                ( ('bb,a a,a a,ccc a,bb,4 bb,d', False, False), 'exception'),
                ( ('bb,a,1 a,a,1 a,ccc a,bb,4 bb,d,5', True, False), 'exception'),
                ( ('b,a,3 a,,4',), 'exception'),
                ( ('b,a,3 a,a,4 c', True, False), "a,a,4 a,b,3 c"),
    ]
    for ( args, solution) in testvals:
        graphString = args[0]
        try:
            g = Graph(*args)
            s = str(g)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                s = 'exception'
        utils.tprint(args, ':', s)
        assert s == solution


def testGraphContains():
    testvals = [
                ( ('',), 'a', False),
                ( ('a',), 'a', True),
                ( ('', False), 'a', False),
                ( ('', False, False), 'a', False),
                ( ('a,a', False), 'b', False),
                ( ('a,a', False), 'a', True),
                ( ('a,b', False), 'a', True),
                ( ('a,b', False), 'b', True),
                ( ('b,a,3 a,a,4', True, False), 'a', True),
                ( ('b,a,3 a,a,4', True, False), 'ab', False),
                ( ('b,a,3 a,a,4',), 'b', True),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), 'ccc', True),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), 'cc', False),
                ( ('b,a,3 a,a,4 z a,ccc,5 b,d,6',), 'z', True),
    ]
    for ( args, node, solution) in testvals:
        graphString = args[0]
        g = Graph(*args)
        val = (node in g)
        utils.tprint(args, node, ':', val)
        assert val == solution

def testGraphIter():
    testvals = [( ('',), [] ),
                ( ('', False), [] ),
                ( ('a,a', False), ['a'] ),
                ( ('a,b', False), ['a', 'b'] ),
                ( ('b,a,3 a,a,4', True, False), ['a', 'b'] ),
                ( ('b,a,3 a,a,4',), ['a', 'b'] ),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), ['a', 'b', 'ccc', 'd'] ),
                ( ('b,a,3 a,a,4 z x a,ccc,5 b,d,6',), ['a', 'b', 'ccc', 'd', 'x', 'z'] ),
    ]
    for ( args, solution) in testvals:
        graphString = args[0]
        g = Graph(*args)
        val = [node for node in g]
        utils.tprint(args,':', val)
        assert sorted(val) == sorted(solution)

def testGraphClone():
    testvals = [ ('',),
                 ('', False),
                 ('a,a', False),
                 ('a,b', False),
                 ('b,a,3 a,a,4', True, False),
                 ('b,a,3 a,a,4',), 
                 ('b,a,3 a,a,4 c d',), 
                 ('bb,a,3 a,a,4 a,ccc,5 bb,d,6', True, True),
                 ('bb,a,3 a,a,4 a,ccc,5 bb,d,6', True, False),
                 ('bb,a a,a a,ccc bb,d', False, True),
                 ('bb,a a,a a,ccc bb,d', False, False),
    ]
    for args in testvals:
        graphString = args[0]
        g = Graph(*args)
        val = g.clone()
        utils.tprint(args,':', val)
        assert g==val
        assert str(g)==str(val)

def testGraphAddNode():
    testvals = [
                ( ('',), 'a', 'a'),
                ( ('a',), 'a', 'exception'),
                ( ('', False), 'a', 'a'),
                ( ('', False, False), 'a', 'a'),
                ( ('a,a', False), 'b', 'a,a b'),
                ( ('a,a', False), 'a', 'exception'),
                ( ('a,b', False), 'a', 'exception'),
                ( ('b,a,3 a,a,4', True, False), 'c', 'a,a,4 b,a,3 c'),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), 'aaa', 'aaa a,a,4 a,ccc,5 b,a,3 b,d,6'),
                ( ('b,a,3 a,a,4', True, False), 'c', 'a,a,4 a,b,3 c'),
    ]
    for ( args, node, solution) in testvals:
        graphString = args[0]
        try:
            g = Graph(*args)
            g.addNode(node)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                g = 'exception'
        utils.tprint(args, node, ':', g)
        if solution != 'exception':
            solution = Graph(solution, *args[1:])
        assert g == solution

def testGetNodesAsSet():
    testvals = [
                ( ('',), []),
                ( ('a',), ['a']),
                ( ('', False), []),
                ( ('', False, False), []),
                ( ('a,a', False), ['a']),
                ( ('a,b', False), ['a', 'b']),
                ( ('b,a,3 a,a,4', True, False), ['a', 'b']),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e',), ['a', 'b', 'ccc', 'd', 'e']),
    ]
    for ( args, solution) in testvals:
        solution = frozenset(solution)
        g = Graph(*args)
        val = g.getNodesAsSet()
        utils.tprint(args, ':', val)
        assert val == solution
    
def testGetEdgesAsDict():
    testvals = [
                ( ('',), {}),
                ( ('a',), {}),
                ( ('', False), {}),
                ( ('', False, False), {}),
                ( ('a,a', False), {Edge(['a', 'a']):1}),
                ( ('a,b', False), {Edge(['a', 'b']):1}),
                ( ('b,a,3 a,a,4', True, False), {Edge(['a', 'b']):3, Edge(['a', 'a']):4}),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e',), {Edge(['b', 'a']):3, Edge(['a', 'a']):4, Edge(['a', 'ccc']):5, Edge(['b', 'd']):6}),
    ]
    for ( args, solution) in testvals:
        g = Graph(*args)
        val = g.getEdgesAsDict()
        utils.tprint(args, ':', val)
        assert val == solution
    
def testGetEdgesAsSet():
    testvals = [
                ( ('',), {}),
                ( ('a',), {}),
                ( ('', False), {}),
                ( ('', False, False), {}),
                ( ('a,a', False), {Edge(['a', 'a']):1}),
                ( ('a,b', False), {Edge(['a', 'b']):1}),
                ( ('b,a,3 a,a,4', True, False), {Edge(['a', 'b']):3, Edge(['a', 'a']):4}),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e',), {Edge(['b', 'a']):3, Edge(['a', 'a']):4, Edge(['a', 'ccc']):5, Edge(['b', 'd']):6}),
    ]
    for ( args, solution) in testvals:
        solution = frozenset(solution.keys())
        g = Graph(*args)
        val = g.getEdgesAsSet()
        utils.tprint(args, ':', val)
        assert val == solution
    
def testEdges():
    testvals = [
                ( ('',), {}),
                ( ('a',), {}),
                ( ('', False), {}),
                ( ('', False, False), {}),
                ( ('a,a', False), {Edge(['a', 'a']):1}),
                ( ('a,b', False), {Edge(['a', 'b']):1}),
                ( ('b,a,3 a,a,4', True, False), {Edge(['a', 'b']):3, Edge(['a', 'a']):4}),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e',), {Edge(['b', 'a']):3, Edge(['a', 'a']):4, Edge(['a', 'ccc']):5, Edge(['b', 'd']):6}),
    ]
    for ( args, solution) in testvals:
        solution = sorted(solution.keys())
        g = Graph(*args)
        val = sorted([e for e in g.edges()])
        utils.tprint(args, ':', val)
        assert val == solution
    
def testNeighbors():
    testvals = [
                ( ('',), 'a', 'exception'),
                ( ('a',),'a', []),
                ( ('', False), 'a', 'exception'),
                ( ('', False, False), 'a', 'exception'),
                ( ('a,a', False), 'a', ['a']),
                ( ('a,b', False), 'a', ['b']),
                ( ('a,b', False), 'b', []),
                ( ('b,a,3 a,a,4', True, False), 'a', ['a', 'b']),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e',), 'e', []),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e a,d,3',), 'a', ['a', 'ccc', 'd']),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e a,d,3',), 'b', ['a', 'd']),
    ]
    for ( args, node, solution) in testvals:
        g = Graph(*args)
        try:
            val = g.neighbors(node)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception'
        utils.tprint(args, node, ':', val)
        if solution != 'exception':
            solution = set(solution)
            val = set(val)
        assert val == solution
    
def testWeightedNeighbors():
    testvals = [
                ( ('',), 'a', 'exception'),
                ( ('a',),'a', {}),
                ( ('b,a,3 a,a,4', True, False), 'a', {'a':4, 'b':3}),
                ( ('b,a,3 a,a,4 a,ccc,5 b,d,6 e',), 'e', {}),
                ( ('b,a,3 a,b,9 a,a,4 a,ccc,5 b,d,6 e a,d,3',), 'a', {'a':4, 'b':9, 'ccc':5, 'd':3}),
                ( ('b,a,3 a,b,9 a,a,4 a,ccc,5 b,d,6 e a,d,3',), 'b', {'a':3, 'd':6}),
    ]
    for ( args, node, solution) in testvals:
        g = Graph(*args)
        try:
            val = g.weightedNeighbors(node)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception'
        utils.tprint(args, node, ':', val, )
        assert val == solution

def testGraphContainsEdge():
    testvals = [
        ( ('',), Edge(['a','b']), False),
        ( ('a',), Edge(['a','a']), False),
        ( ('', False), Edge(['a','b']), False),
        ( ('', False, False), Edge(['a','b']), False),
        ( ('a,a', False), Edge(['b','a']), False),
        ( ('a,a', False), Edge(['a','a']), True),
        ( ('a,b', False), Edge(['a','b']), True),
        ( ('a,b', False), Edge(['b','a']), False),
        ( ('b,a,3 a,a,4', True, False), Edge(['a','b']), True),
        ( ('b,a,3 a,a,4', True, False), Edge(['ab','a']), False),
        ( ('b,a,3 a,a,4',), Edge(['b','a']), True),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), Edge(['a','ccc']), True),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), Edge(['ccc','a']), False),
        ( ('b,a,3 a,a,4 z a,ccc,5 b,d,6',), Edge(['z','z']), False),
    ]
    for ( args, edge, solution) in testvals:
        g = Graph(*args)
        val = g.containsEdge(edge)
        utils.tprint(args, edge, ':', val)
        assert val == solution

def testGetWeight():
    testvals = [
        ( ('',), Edge(['a','b']), 'exception'),
        ( ('a',), Edge(['a','a']), 'exception'),
        ( ('a,b,4 a,c,5',), Edge(['a','a']), 'exception'),
        ( ('b,a,3 a,a,4', True, False), Edge(['a','b']), 3),
        ( ('b,a,3 a,a,4',), Edge(['b','a']), 3),
        ( ('b,a,3 a,a,4',), Edge(['a','b']), 'exception'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), Edge(['a','ccc']), 5),
        ( ('b,a,3 a,b,9 a,a,4 a,ccc,5 b,d,6',), Edge(['b','a']), 3),
        ( ('b,a,3 a,b,9 a,a,4 z a,ccc,5 b,d,6',), Edge(['a','b']), 9),
    ]
    for ( args, edge, solution) in testvals:
        g = Graph(*args)
        try:
            val = g.getWeight(edge)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception'
        utils.tprint(args, edge, ':', val, )
        assert val == solution

def testGraphAddEdge():
    testvals = [
        ( ('',), Edge(['a','b']), 'exception'),
        ( ('a',), Edge(['a','a']), 'a,a,1'),
        ( ('a,a b', False), Edge(['b','a']), 'a,a b,a'),
        ( ('a,a', False), Edge(['a','a']), 'exception'),
        ( ('a,b', False), Edge(['a','b']), 'exception'),
        ( ('a,b', False), Edge(['b','a']), 'a,b b,a'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), (Edge(['a','ccc']),9), 'exception'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), (Edge(['ccc','a']),9), 'ccc,a,9 b,a,3 a,a,4 a,ccc,5 b,d,6'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6', True, False), (Edge(['b','ccc']),9), 'b,ccc,9 b,a,3 a,a,4 a,ccc,5 b,d,6'),
        ( ('b,a,3 a,a,4 z a,ccc,5 b,d,6',), Edge(['z','z']), 'b,a,3 a,a,4 z,z,1 a,ccc,5 b,d,6'),
    ]
    for ( args, edgeArgs, solution) in testvals:
        g = Graph(*args)
        if isinstance(edgeArgs, Edge):
            edgeArgs = tuple(edgeArgs,)

        try:
            g.addEdge(*edgeArgs)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                g = 'exception'

        solnArgs = list(args)
        solnArgs[0] = solution
        if solution != 'exception':
            solution = Graph(*solnArgs)
        utils.tprint(args, edgeArgs, ':', g)
        assert g == solution

def testGraphRemoveEdge():
    testvals = [
        ( ('',), Edge(['a','b']), 'exception'),
        ( ('a',), Edge(['a','a']), 'exception'),
        ( ('a,a b', False), Edge(['a','a']), 'a b'),
        ( ('a,a', False), Edge(['a','a']), 'a'),
        ( ('a,b', False), Edge(['a','b']), 'a b'),
        ( ('a,b', False), Edge(['b','a']), 'exception'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), Edge(['a','ccc']), 'ccc b,a,3 a,a,4 b,d,6'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6',), Edge(['ccc','a']), 'exception'),
        ( ('b,a,3 a,a,4 a,ccc,5 b,d,6', True, False), Edge(['d','b']), 'd b,a,3 a,a,4 a,ccc,5'),
    ]
    for ( args, edge, solution) in testvals:
        g = Graph(*args)

        try:
            g.removeEdge(edge)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                g = 'exception'

        solnArgs = list(args)
        solnArgs[0] = solution
        if solution != 'exception':
            solution = Graph(*solnArgs)
        utils.tprint(args, edge, ':', g)
        assert g == solution


def testGraphIsPath():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 e,a,5 c,c,6 z'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)
    g3 = g1.clone(); g3.addEdge(Edge(['b','a']))

    testvals = [
        ( (Graph(''), ''), True),
        ( (Graph('a'), ''), True),
        ( (Graph('a'), 'a'), True),
        ( (Graph('a,a,1'), 'a,a'), True),
        ( (g1, 'a,b'), True),
        ( (g1, 'b,a'), False),
        ( (g2, 'b,a'), True),
        ( (g1, 'z'), True),
        ( (g2, 'z'), True),
        ( (g1, 'a'), True),
        ( (g2, 'a'), True),
        ( (g1, 'c'), True),
        ( (g2, 'c'), True),
        ( (g1, 'c,c'), True),
        ( (g2, 'c,c'), True),
        ( (g1, 'a,b,c'), True),
        ( (g2, 'a,b,c'), True),
        ( (g1, 'c,b,a'), False),
        ( (g2, 'c,b,a'), True),
        ( (g1, 'a,b,c,c'), True),
        ( (g2, 'a,b,c,c'), True),
        ( (g1, 'a,b,c,c,c'), False),
        ( (g2, 'a,b,c,c,c'), False),
        ( (g1, 'a,b,c,c,d,e,a'), True),
        ( (g2, 'a,b,c,c,d,e,a'), True),
        ( (g1, 'a,b,c,c,d,e,a,b'), False),
        ( (g2, 'a,b,c,c,d,e,a,b'), False),
        ( (g1, 'a,b,a'), False),
        ( (g2, 'a,b,a'), False),
        ( (g3, 'a,b,a'), True),
        ( (g3, 'a,b,a,b'), False),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        path = Path.fromString(pathStr)
        val = g.isPath(path)
        utils.tprint(args, ':', val)
        assert val == solution

def testGraphIsCycle():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 e,a,5 c,c,6 z'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)
    g3 = g1.clone(); g3.addEdge(Edge(['b','a']))

    testvals = [
        ( (Graph(''), ''), True),
        ( (Graph('a'), ''), True),
        ( (Graph('a'), 'a'), False),
        ( (Graph('a,a,1'), 'a'), True),
        ( (g1, 'a,b'), False),
        ( (g1, 'b,a'), False),
        ( (g3, 'a,b'), True),
        ( (g2, 'a,b'), False),
        ( (g2, 'b,a'), False),
        ( (g1, 'z'), False),
        ( (g2, 'z'), False),
        ( (g1, 'a'), False),
        ( (g2, 'a'), False),
        ( (g1, 'c'), True),
        ( (g2, 'c'), True),
        ( (g1, 'c,c'), False),
        ( (g2, 'c,c'), False),
        ( (g1, 'a,b,c'), False),
        ( (g2, 'a,b,c'), False),
        ( (g1, 'c,b,a'), False),
        ( (g2, 'c,b,a'), False),
        ( (g1, 'a,b,c,d,e'), True),
        ( (g2, 'a,b,c,d,e'), True),
        ( (g1, 'a,b,c,c,d,e'), True),
        ( (g2, 'a,b,c,c,d,e'), True),
        ( (g1, 'a,b,c,c,d,e,a'), False),
        ( (g2, 'a,b,c,c,d,e,a'), False),
        ( (g1, 'a,b,a'), False),
        ( (g2, 'a,b,a'), False),
        ( (g3, 'a,b,a'), False),
        ( (g3, 'a,b,a,b'), False),
        ( (Graph('a,a,1'), 'a'), True),
        ( (Graph('a,a,1'), 'a,a'), False),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        path = Path.fromString(pathStr)
        val = g.isCycle(path)
        utils.tprint(args, ':', val)
        assert val == solution

def testContainsAllNodesOnce():
    graphStr1 = ''
    graphStr2 = 'a'
    graphStr3 = 'a,a,1'
    graphStr4 = 'a,b,1'
    graphStr5 = 'a,b,1 b,c,2 c,d,3 d,e,4 e,a,5 c,c,6 z'
    g1 = Graph(graphStr1)
    g2 = Graph(graphStr2)
    g3 = Graph(graphStr3)
    g4 = Graph(graphStr4)
    g5 = Graph(graphStr5)

    testvals = [
        ( (g1, ''), True),
        ( (g1, 'a'), False),
        ( (g2, ''), False),
        ( (g2, 'a,b'), False),
        ( (g2, 'a'), True),
        ( (g3, ''), False),
        ( (g3, 'a,b'), False),
        ( (g3, 'a,a'), False),
        ( (g3, 'a'), True),
        ( (g4, ''), False),
        ( (g4, 'a,b'), True),
        ( (g4, 'a'), False),
        ( (g4, 'a,a'), False),
        ( (g4, 'a,b,c'), False),
        ( (g5, 'a,b,c,d,e,z'), True),
        ( (g5, 'a,b,c,d,e'), False),
        ( (g5, 'a,b,c,d,e,z,a'), False),
        ( (g5, 'a,b,c,d,e,z,y'), False),
        ( (g5, 'a,b,c,d,f,z'), False),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        nodes = pathStr.split(',') if len(pathStr)>0 else []
        path = Path(nodes)
        val = g.containsAllNodesOnce(path)
        utils.tprint(args, ':', val)
        assert val == solution

def testGraphIsHamiltonPath():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 c,c,6'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)

    testvals = [
        ( (Graph(''), ''), True),
        ( (Graph('a'), ''), False),
        ( (Graph('a'), 'a'), True),
        ( (Graph('a,a,1'), 'a,a'), False),
        ( (g1, 'a,b'), False),
        ( (g1, 'a,b,c'), False),
        ( (g2, 'a,b,c'), False),
        ( (g1, 'a,b,c,d,e'), True),
        ( (g2, 'a,b,c,d,e'), True),
        ( (g1, 'a,b,c,c,d,e'), False),
        ( (g2, 'a,b,c,c,d,e'), False),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        path = Path.fromString(pathStr)
        val = g.isHamiltonPath(path)
        utils.tprint(args, ':', val)
        assert val == solution

def testGraphIsHamiltonCycle():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 c,c,6'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)
    g3 = g1.clone(); g3.addEdge(Edge(['e','a']))
    g3b = g1.clone(); g3b.addEdge(Edge(['a','e']))
    g4 = g2.clone(); g4.addEdge(Edge(['a','e']))

    testvals = [
        ( (Graph(''), ''), True),
        ( (Graph('a'), ''), False),
        ( (Graph('a'), 'a'), False),
        ( (Graph('a,a', weighted=False), 'a'), True),
        ( (Graph('a,a,1'), 'a'), True),
        ( (Graph('a,a,1'), 'a,a'), False),
        ( (g1, 'a,b'), False),
        ( (g1, 'a,b,c'), False),
        ( (g2, 'a,b,c'), False),
        ( (g1, 'a,b,c,d,e'), False),
        ( (g2, 'a,b,c,d,e'), False),
        ( (g3, 'a,b,c,d,e'), True),
        ( (g3b, 'a,b,c,d,e'), False),
        ( (g4, 'a,b,c,d,e'), True),
        ( (g3, 'a,b,c,c,d,e'), False),
        ( (g4, 'a,b,c,c,d,e'), False),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        path = Path.fromString(pathStr)
        val = g.isHamiltonCycle(path)
        utils.tprint(args, ':', val)
        assert val == solution

    
def testGraphIsClique():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 a,c,7 a,d,8 c,c,6'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)
    g1b = g1.clone()
    g1b.addEdge(Edge(['b','a']))
    g1b.addEdge(Edge(['c','a']))
    g1b.addEdge(Edge(['c','b']))
    g3 = Graph('a,b a,c a,d b,c b,d c,d a,e b,e c,e', weighted=False, directed=False)

    testvals = [
        ( (Graph(''), ''), True),
        ( (Graph('a'), ''), True),
        ( (Graph('a'), 'a'), True),
        ( (Graph('a,a,1'), 'a'), True),
        ( (Graph('a,a,1'), 'a,a'), True),
        ( (g1, 'a'), True),
        ( (g2, 'a'), True),
        ( (g1, 'a,b'), False),
        ( (g2, 'a,b'), True),
        ( (g1, 'a,b,c'), False),
        ( (g2, 'a,b,c'), True),
        ( (g1, 'a,b,c,d'), False),
        ( (g2, 'a,b,c,d'), False),
        ( (g1b, 'a,b'), True),
        ( (g1b, 'a,b,c'), True),
        ( (g1b, 'a,b,c,d'), False),
        ( (g3, 'a,b,c,d'), True),
        ( (g3, 'a,b,c,d,e'), False),
    ]
    for ( args, solution) in testvals:
        g, nodesStr = args
        nodes = nodesStr.split(',') if len(nodesStr)>0 else []
        val = g.isClique(nodes)
        utils.tprint(args, ':', val)
        assert val == solution

def testGraphConvertToWeighted():
    g1 = Graph('a,b a,c a,d', weighted=False, directed=False)
    g2 = Graph('a,b a,c a,d', weighted=False, directed=True)
    g3 = Graph('a,b,1 a,c,1 a,d,1', weighted=True, directed=False)
    g4 = Graph('a,b,1 a,c,1 a,d,1', weighted=True, directed=True)

    testvals = [
        ( g1, g3),
        ( g2, g4),
    ]
    for ( g, solution) in testvals:
        val = g.clone()
        val.convertToWeighted()
        utils.tprint(g, ':', val)
        assert val == solution

def testGraphConvertToDirected():
    g1 = Graph('a,b a,c a,d', weighted=False, directed=False)
    g2 = Graph('a,b a,c a,d b,a c,a d,a', weighted=False, directed=True)
    g3 = Graph('a,b,1 a,c,1 a,d,1', weighted=True, directed=False)
    g4 = Graph('a,b,1 a,c,1 a,d,1 b,a,1 c,a,1 d,a,1', weighted=True, directed=True)

    testvals = [
        ( g1, g2),
        ( g3, g4),
    ]
    for ( g, solution) in testvals:
        val = g.clone()
        val.convertToDirected()
        utils.tprint(g, ':', val)
        assert val == solution

def testGraphPathLength():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 e,a,5 c,c,6 z'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)

    testvals = [
        ( (Graph(''), ''), 0),
        ( (Graph('a'), ''), 0),
        ( (Graph('a'), 'a'), 0),
        ( (Graph('a,a,1'), 'a,a'), 1),
        ( (g1, 'a,d'), 'exception'),
        ( (g1, 'a,b'), 1),
        ( (g1, 'b,a'), 'exception'),
        ( (g2, 'b,a'), 1),
        ( (g1, 'a,b,c,d,e'), 10),
        ( (g2, 'a,b,c,d,e'), 10),
        ( (g1, 'a,b,c,c,d,e'), 16),
        ( (g2, 'a,b,c,c,d,e'), 16),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        path = Path.fromString(pathStr)
        try:
            val = g.pathLength(path)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception'
        utils.tprint(args, ':', val)
        assert val == solution


def testGraphCycleLength():
    graphStr = 'a,b,1 b,c,2 c,d,3 d,e,4 e,a,5 c,c,6 z'
    g1 = Graph(graphStr)
    g2 = Graph(graphStr, directed=False)

    testvals = [
        ( (Graph(''), ''), 0),
        ( (Graph('a'), ''), 0),
        ( (Graph('a'), 'a'), 'exception'),
        ( (Graph('a,a,1'), 'a'), 1),
        ( (Graph('a,a,1'), 'a,a'), 'exception'),
        ( (g1, 'a,d'), 'exception'),
        ( (g1, 'a,b'), 'exception'),
        ( (g1, 'c'), 6),
        ( (g1, 'a,b,c,d,e'), 15),
        ( (g2, 'a,b,c,d,e'), 15),
    ]
    for ( args, solution) in testvals:
        g, pathStr = args
        path = Path.fromString(pathStr)
        try:
            val = g.cycleLength(path)
        except utils.WcbcException as e:
            if solution != 'exception':
                raise e
            else:
                val = 'exception'
        utils.tprint(args, ':', val)
        assert val == solution

def testGraphChooseNode():
    testvals = [
        ( Graph(''), {}),
        ( Graph('a'), {'a'}),
        ( Graph('a,a,1'), {'a'}),
        ( Graph('a,b,1'), {'a','b'}),
        ( Graph('a,b,1 b,c,1'), {'a','b','c'}),
    ]
    for ( g, solution) in testvals:
        val = g.chooseNode()
        utils.tprint(g, ':', val)
        if len(solution)==0:
            assert val == None
        else:
            assert val in solution

def testGraphSumEdgeWeights():
    g1 = Graph('a,b a,c a,d', weighted=False, directed=False)
    g2 = Graph('a,b a,c a,d', weighted=False, directed=True)
    g3 = Graph('a,b,1 a,c,2 a,d,3', weighted=True, directed=False)
    g4 = Graph('a,b,1 a,c,2 a,d,3 b,a,4', weighted=True, directed=True)

    testvals = [
        ( Graph(''), 0),
        ( Graph('a'), 0),
        ( Graph('a,a,5'), 5),
        ( g1, 3),
        ( g2, 3),
        ( g3, 6),
        ( g4, 10),
    ]
    for ( g, solution) in testvals:
        val = g.sumEdgeWeights()
        utils.tprint(g, ':', val)
        assert val == solution


    

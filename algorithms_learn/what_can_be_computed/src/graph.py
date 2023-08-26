import utils; from utils import rf
from utils import WcbcException

class Path:
    """A Path object models a path in a graph.
    """
    def __init__(self, nodes):
        """Initialize Path object.
        
        Args:

            nodes (list of str): a list containing the names of the nodes in the path
        """
        if isinstance(nodes, str):
            raise WcbcException('Path constructor parameter must be a list, not a string')
        for node in nodes:
            if not isinstance(node, str):
                raise WcbcException('Path node', str(node), 'isn\'t a string')
            if len(node)==0:
                raise WcbcException('Encountered empty node name')

        self.nodes = tuple(nodes)
        """Tuple of the nodes in the path, where each node is a string."""

        self.nodeSet = None
        """A set of str that is constructed lazily (if and when needed). 
        It will contain the nodes in the path"""
                
        self.edgeSet = None
        """Set of Edge objects in the path. 
        Constructed lazily (if and when needed)."""

    def __str__(self):
        return ','.join(self.nodes)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        """Return the number of nodes in the path"""
        return len(self.nodes)

    def __getitem__(self,index):
        """Return the index-th node in the path"""
        return self.nodes[index]

    # Iterates over edges, not nodes.
    def __iter__(self):
        """Iterate over the Edge objects in the path"""
        return PathIterator(self)

    # Determines membership of node, not edge. Inconsistent with
    # __iter__(), but too bad! Very bad Python!!
    def __contains__(self, node):
        """Return True if node is in this path, and False otherwise."""
        if self.nodeSet == None:
            self.nodeSet = frozenset(self.nodes)
        return node in self.nodeSet

    def __eq__(self, other):
        if self is other: return True
        if other==None: return False
        # Importantly, we allow subclasses to be equal -- this allows
        # an equivalent Path and Edge to be equal.
        if not isinstance(other, Path): return False
        return self.nodes==other.nodes

    def __ne__(self, other):
        return not self==other

    def __lt__ (self, other):
        return self.nodes < other.nodes

    def __gt__ (self, other):
        return other.__lt__(self)

    def __hash__(self):
        return self.nodes.__hash__()

    # static function, constructs a new Path object from a string such
    # as 'a,b,c'
    @staticmethod
    def fromString(pathStr):
        """Construct a new Path object from a string and return it.

        Args:

            pathStr (str): This string should list the nodes in the
                path separated by commas. For example:
                'apple,banana,x,y,z' yields a path consisting of five
                nodes and four edges.

        Returns:

            Path: A new Path object.

        """
        return Path(pathStr.split(',') if pathStr!='' else [])
    
    
    def start(self):
        """Return the initial node in the path.

        Returns: 

           str: the initial node in the path.

        """
        if len(self.nodes)==0:
            raise WcbcException('can\'t find start of empty path')
        return self.nodes[0]

    def end(self):
        """Return the final node in the path.

        Returns: 

           str: the final node in the path.

        """
        if len(self.nodes)==0:
            raise WcbcException('can\'t find end of empty path')
        return self.nodes[-1]

    def extend(self, node):
        """Extend the current path by appending the given node.

        Args:

            node (str): The node to be added.

        Returns:

            Path: A new Path object with the given node appended.

        """
        return Path( self.nodes + (node,) )

    def reverse(self):
        """Reverse of the current path.

        Returns:

            Path: A new Path object which is the reverse of the current path.

        """
        return Path( tuple(reversed(self.nodes)) )


    def rotateToFront(self, node):
        """Cyclically permute the nodes in the path so that a given node is at
the start of the path.

        Args:

            node (str): The node which should be at the start of the
            path. An exception will be thrown if it is not currently
            in the path.

        Returns:

            Path: A new Path object, cyclically permuted so the given
            node is at the start of the path.

        """
        if not node in self.nodes:
            raise WcbcException('node ' + str(node) + ' is not in the path ' + str(self))
        ind = self.nodes.index(node)
        newNodes = self.nodes[ind:] + self.nodes[:ind]
        return Path(newNodes)

    def containsEdge(self, edge):
        """Return True if the given edge is in this path and False otherwise.

        Args:

            edge (Edge): The edge we are querying.

        Returns:

            bool: True if the given edge is in this path and False otherwise.

        """
        if self.edgeSet == None:
            self.edgeSet = set([e for e in self])
        return edge in self.edgeSet

class PathIterator:
    """Iterator class for iterating over the edges in a Path."""
    
    def __init__(self, path):
        """Initialize a PathIterator.

        Args:

            path (Path): The path over whose edges we will be
                iterating.

        """
        self.path = path
        self.counter = 0
        if len(path)<=1:
            self.short = True
        else:
            self.short = False

    def __next__(self):
        self.counter += 1
        if self.short or self.counter == len(self.path):
            raise StopIteration
        node1 = self.path[self.counter-1]
        node2 = self.path[self.counter]
        return Edge( (node1, node2) )

    next = __next__  # for Python 2; see https://stackoverflow.com/questions/29578469/how-to-make-an-object-both-a-python2-and-python3-iterator
    
class Edge(Path):
    """An Edge object represents an edge in a path or graph. It is
    implemented as a Path with exactly 2 nodes, so it inherits all of
    the methods and properties of Path.

    """
    def __init__(self, nodes):
        Path.__init__(self, nodes)
        assert len(nodes)==2

class Graph:
    """A Graph object represents a graph i.e., a collection of nodes with edges between them.

    The graph may be weighted or unweighted, directed or undirected.

    """
    def __init__(self, graphString, weighted=True, directed=True):
        """Initialize Graph object.
        
        Args:

            graphString (str): a description of the graph as an ASCII
                string, as described in the textbook. Examples include
                'a,b b,c c,a' and 'a,b,4 b,c,3'.

            weighted (bool): True if this is a weighted graph and False otherwise.

            directed (bool): True if this is a directed graph and False otherwise.

        """
        self.weighted = weighted
        self.directed = directed

        self.nodes = dict()
        """A dictionary storing the structure of the graph. It maps strings to
        dictionaries. Each key is a node name n, and the corresponding
        value self.nodes[n] is a dictionary of outgoing edges leaving
        n. Each of these dictionaries of outgoing edges maps strings
        to integers: each key in self.nodes[n] is a neighbor m of n,
        and the value self.nodes[n][m] is the weight of the edge from
        n to m.

        """

        self.readDescription(graphString)
        
        self.isolatedNodes = None 
        """A frozenset of strings. Each element is an isolated node, i.e. a
        node with no incoming or outgoing edges. This will be computed
        lazily, on demand.

        """

    def __eq__(self, other):
        if self is other: return True
        if other==None: return False
        if not isinstance(other, Graph): return False
        return self.nodes==other.nodes and \
            self.directed==other.directed and \
            self.weighted==other.weighted 

    def __ne__(self, other):
        return not self==other

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
        edgeStrings = []
        for edge, weight in self.getEdgesAsDict().items():
            if self.weighted:
                edgeString = str(edge) + ',' + str(weight)
            else:
                edgeString = str(edge)
            edgeStrings.append(edgeString)
        edgesAndIsolatedNodes = edgeStrings + list(self.getIsolatedNodes())
        graphString = ' '.join(sorted(edgesAndIsolatedNodes))
        return graphString

    def __repr__(self):
        return self.__str__()

    def __contains__(self, node):
        return node in self.nodes

    def __iter__(self):
        return iter(self.nodes)

    def readDescription(self, graphString):
        """Read the given ASCII description of a graph, storing information about the nodes and edges.

        This is intended to be a private method called by
        __init__(). It will update self.nodes, which should be an
        empty dictionary when this method is called.

        Args:

            graphString (str): a description of the graph as an ASCII
                string, as described in the textbook. Examples include
                'a,b b,c c,a' and 'a,b,4 b,c,3'.

        """
        edgeDescriptions = [x.strip() for x in graphString.split()]
        for edgeDescription in edgeDescriptions:
            if len(edgeDescription)>0:
                components = edgeDescription.split(',')
                if len(components)==1:
                    # isolated node with no edges (yet)
                    (sourceStr, destStr, weightStr) = (components[0], None, None)
                elif self.weighted:
                    if len(components)!=3:
                        raise WcbcException('expected 3 components in edge description ' \
                                            + edgeDescription + \
                                            'for weighted graph')
                    (sourceStr, destStr, weightStr) = edgeDescription.split(',')
                    weight = int(weightStr)
                else:
                    if len(components)!=2:
                        raise WcbcException('expected 2 components in edge description ' \
                                            + edgeDescription + \
                                            'for unweighted graph')
                    (sourceStr, destStr) = edgeDescription.split(',')
                    weight = 1

                if len(sourceStr)==0 or (destStr and len(destStr)==0): 
                    raise WcbcException('encountered node name of length zero')
                
                if not sourceStr in self.nodes: 
                    self.nodes[sourceStr] = dict()
                source = self.nodes[sourceStr]
                if destStr!=None:
                    if not destStr in self.nodes:
                        # we haven't seen this node before -- create it
                        self.nodes[destStr] = dict()
                    if destStr in source:
                        raise WcbcException('duplicate edge ' + str([sourceStr, destStr]))
                    source[destStr] = weight
                    if not self.directed:
                        dest = self.nodes[destStr]
                        if sourceStr in dest and sourceStr!=destStr:
                            raise WcbcException('duplicate edge ' + str([destStr, sourceStr]))
                        dest[sourceStr] = weight
    
    def clone(self):
        """Return a new Graph object identical to the current one.

        """
        
        # inefficient, but extremely easy to implement!
        return Graph(str(self), self.weighted, self.directed)

    def getIsolatedNodes(self):
        """Return a frozenset consisting of nodes with no incoming or
outgoing edges.

            Returns:

                frozenset of str: nodes with no incoming or outgoing
                    edges

        """
        if not self.isolatedNodes: # need to update
            self.isolatedNodes = self.computeIsolatedNodes()
        return self.isolatedNodes

    def computeIsolatedNodes(self):
        """Private method that computes the set of isolated nodes.

            Returns:

                frozenset of str: the set of isolated nodes
        """
        isolated = set(self.nodes.keys())
        for node, neighbors in self.nodes.items():
            if len(neighbors)>0:
                # print('discarding', node, 'because len(neighbors)>0')
                isolated.discard(node)
            for neighbor, weight in neighbors.items():
                # print('discarding', neighbor, 'because nbr of', node)
                isolated.discard(neighbor)
        # print('computeIsolatedNodes:', isolated)
        return frozenset(isolated)
                

    def addNode(self, node):
        """Add the given node to the graph.

        The node is added to the graph as an isolated node with no
        incoming or outgoing edges.

        Args:

            node (str): The node to be added.

        """
        if node in self.nodes:
            raise WcbcException('Tried to add existing node ' + node)
        self.nodes[node] = dict()
        self.isolatedNodes = None # force recomputation later, when needed

    def getNodesAsSet(self):
        """Return a frozenset consisting of all nodes in the graph.

            Returns:

                frozenset of str: elements are the nodes in the graph

        """
        return frozenset(self.nodes.keys())


    # key will be an Edge object, value will be weight
    def getEdgesAsDict(self):
        """Return a dictionary of edges and weights in the graph.

            Returns:

                dict mapping Edge to int: Each key is an Edge object,
                    and its corresponding value is the weight of that
                    edge.

        """
        edges = dict()
        for node, neighbors in self.nodes.items():
            for neighbor, weight in neighbors.items():
                edge = Edge([node,neighbor])
                reversedEdge = Edge([neighbor,node])
                # If undirected, store only one direction. By
                # convention, this will be the lexicographically
                # earlier one.
                if not self.directed and reversedEdge < edge:
                    edge = reversedEdge
                # Now store the edge
                edges[edge] = weight
        return edges

    def getEdgesAsSet(self):
        """Return a frozenset of edges in the graph.

            Returns:

                frozenset of Edge: the edges in the graph.

        """
        return frozenset([e for e in self.getEdgesAsDict()])

    def edges(self):
        """Return an iterable that will iterate over all edges in the graph.

            Returns:

                iterable of Edge: the edges in the graph.

        """

        # At present this method is implemented via getEdgesAsSet,
        # which is obviously inefficient from the point of view of
        # memory usage---it makes a copy of all the edges. It would be
        # possible to implement a more complex, but more
        # memory-efficient, iterator for edges.
        return self.getEdgesAsSet()

    def neighbors(self, node):
        """Return a set-like view of the neighbors of a given node.

        The neighbors of node n are defined to be all nodes that are
        at the end of outgoing edges from n.

        Args:

            node (str): The node whose neighbors will be returned.

        Returns:

            dictionary view of str: The returned object is a
                dictionary view (see Python documentation on
                "dictionary view objects"). Iterating over this view
                will yield all nodes at the end of outgoing edges from
                the given parameter node.

        """
        
        if not node in self:
            raise WcbcException('node ' + node + ' not in graph')
        return self.nodes[node].keys()

    def weightedNeighbors(self, node):
        """Return a dictionary of the neighbors of a given node with weights as keys.

        The neighbors of node n are defined to be all nodes that are
        at the end of outgoing edges from n.

        Args:

            node (str): The node n whose neighbors will be returned.

        Returns:

            dictionary mapping str to int: Each key in the dictionary
                is a neighbor m of n, i.e. there is an edge from n to
                m. The value corresponding to key m is the weight of
                the edge n to m.

        """
        if not node in self:
            raise WcbcException('node ' + node + ' not in graph')
        return self.nodes[node]

    def containsEdge(self, edge):
        """Return True if the graph contains the given edge and False otherwise.

        Args:

            edge (Edge): the edge to be searched for

        Returns:

            bool: True if the graph contains the given edge and False otherwise

        """
        node1, node2 = edge.nodes
        if node1 not in self.nodes or node2 not in self.nodes:
            return False
        if node2 in self.nodes[node1]:
            return True
        elif not self.directed and node1 in self.nodes[node2]:
            return True
        else:
            return False

    def getWeight(self, edge):
        """Return the weight of the given edge.

        An exception is thrown if the edge is not present.

        Args:

            edge (Edge): the edge to be searched for

        Returns:

            int: The weight of the given edge.

        """
        if not self.containsEdge(edge):
            raise WcbcException('edge ' + str(edge) + ' not in graph')
        node1, node2 = edge.nodes
        return self.nodes[node1][node2]

    def addEdge(self, edge, weight = 1):
        """Add an edge to the graph.

        An exception is thrown if the edge is already present. An
        exception is also thrown if the edge contains a node that is
        not in the graph.

        Args:

            edge (Edge): the edge to be added

            weight (int): the weight of the edge to be added

        """
        node1, node2 = edge.nodes
        if self.containsEdge(edge):
            raise WcbcException('edge ' + str(edge) + ' already in graph')
        if not node1 in self:
            raise WcbcException('node ' + node1 + ' not in graph')
        if not node2 in self:
            raise WcbcException('node ' + node2 + ' not in graph')

        self.nodes[node1][node2] = weight
        if not self.directed:
            self.nodes[node2][node1] = weight
        self.isolatedNodes = None # force recomputation later, when needed

    def removeEdge(self, edge):
        """Remove an edge from the graph.

        An exception is thrown if the edge is not already
        present. This implicitly requires that both nodes in the edge
        are also present.

        Args:

            edge (Edge): the edge to be removed

        """
        node1, node2 = edge.nodes
        if not self.containsEdge(edge):
            raise WcbcException('edge ' + str(edge) + ' not in graph')

        if node2 in self.nodes[node1]: del self.nodes[node1][node2]  
        if not self.directed:
            if node1 in self.nodes[node2]: del self.nodes[node2][node1] 
        self.isolatedNodes = None # force recomputation later, when needed
        
    def isPath(self, path, source = None, dest = None):
        """Return true if the given path exists as a simple path in the current graph.

        The path passed in as a parameter is just a sequence of
        nodes. The question is, does each consecutive pair of nodes in
        that sequence exist as an edge in the current graph?
        Optionally, we can also check whether the start and end of the
        path correspond to particular nodes.

        Note that this method does not permit paths to have repeated
        edges i.e. it returns True only if the given path is a
        **simple** path. Perhaps the method would be better named
        isSimplePath(), but for the purposes of the textbook we are
        only interested in simple paths and it seems easier to stick
        with a short method name.

        Args:

            path (Path): the sequence p of nodes to be investigated

            source (str): the name of the node that will be checked to
                see if it is the start of the path, or None to skip
                this check

            dest (str): the name of the node that will be checked to
                see if it is the end of the path, or None to skip
                this check

        Returns:

            bool: True if p exists as a simple path in the current
                graph, and False otherwise. In addition, if source is
                specified, we return False unless the given source is
                the start of p. Similarly, if dest is specified, we
                return False unless the given dest is the end of p.

        """
        if len(path)==0: 
            return True
        if source == None: 
            source = path.start()
        if dest == None: 
            dest = path.end()
        if path.start() != source or path.end() != dest:
            return False
        # use a set to check for repeated edges, which aren't allowed
        # in our definition of a path
        edges = set()
        for edge in path:
            if not self.containsEdge(edge):
                return False
            # repeated edges are not allowed
            if edge in edges:
                return False
            # remember this edge, and its reverse if this is not a
            # directed graph
            edges.add(edge)
            if not self.directed:
                edges.add(edge.reverse())
        return True

    def isCycle(self, path):
        """Return True if the given path exists as a simple cycle in the current graph.

        The path passed in as a parameter is just a sequence of
        nodes. The question is, does each consecutive pair of nodes in
        that sequence exist as an edge in the current graph, and is
        there also an edge from the final node to the initial node?

        Note that this method does not permit cycles to have repeated
        edges i.e. it returns True only if the given cycle is a
        **simple** cycle. Perhaps the method would be better named
        isSimpleCycle(), but for the purposes of the textbook we are
        only interested in simple cycles and it seems easier to stick
        with a short method name.

        Another very important note is our convention for representing
        cycles: the "final edge" (from the last node in the cycle back
        to the first node) is not explicitly represented in the
        sequence of nodes passed as a parameter. The final edge is
        assumed implicitly to be part of the cycle. If that final edge
        is explicitly present in the passed parameter, this method
        will return False, because it does not in fact represent a
        cycle once the implicit final edge has also been added.

        Args:

            path (Path): the sequence p of nodes to be investigated

        Returns:

            bool: True if p exists as a simple cycle in the current
                graph (once the implicit final edge is added), and
                False otherwise.

        """
        if len(path)==0: 
            return True
        if not self.isPath(path):
            return False
        finalEdge = Edge([path.end(), path.start()])
        if not self.containsEdge(finalEdge):
            return False
        # repeated edge is not permitted in a cycle
        if path.containsEdge(finalEdge):
            return False
        if not self.directed and path.containsEdge(finalEdge.reverse()):
            return False
        return True

    def containsAllNodesOnce(self, path):
        """Return True if the given path contains all nodes in the current graph exactly once.

        Args:

            path (Path): the sequence p of nodes to be investigated

        Returns:

            bool: True if p contains all nodes in the current graph exactly once.

        """
        
        # check that all graph nodes are contained in the path
        for node in self.nodes:
            if node not in path:
                return False
        # check that all path nodes are contained in the graph
        for node in path.nodes:
            if node not in self.nodes:
                return False
            
        # It's possible that some nodes were repeated. An easy way to
        # check for this is to see if the number of nodes in the path
        # is the same as the number of nodes in the graph.
        if len(path) != len(self):
            return False
        return True

    def isHamiltonPath(self, path):
        """Return True if the given path is a Hamilton path in the current graph.

        Args:

            path (Path): the sequence p of nodes to be investigated

        Returns:

            bool: True if p is a Hamilton path in the current graph.

        """
        
        if not self.isPath(path):
            return False
        if not self.containsAllNodesOnce(path):
            return False
        return True

    def isHamiltonCycle(self, path):
        """Return True if the given path is a Hamilton cycle in the current graph.

        See the important note in the documentation for isCycle(): the
        given path parameter should not explicitly contain the final
        edge back to the start of the cycle; it will be added
        implicitly.

        Args:

            path (Path): the sequence p of nodes to be investigated

        Returns:

            bool: True if p is a Hamilton cycle in the current graph.

        """
        
        if not self.isCycle(path):
            return False
        if not self.containsAllNodesOnce(path):
            return False
        return True

    def isClique(self, nodes):
        """Return True if the given collection of nodes forms a clique in the current graph.

        Args:

            nodes (iterable of str): the collection of nodes to be investigated

        Returns:

            bool: True if the given collection of nodes forms a clique
                in the current graph.

        """
        
        for node1 in nodes:
            for node2 in nodes:
                if node1 != node2:
                    if not self.containsEdge( Edge([node1, node2]) ):
                        return False
        return True

    def convertToWeighted(self):
        """Convert the current graph to a weighted graph.

        If the graph is already weighted, it will be unchanged. If it
        is unweighted, it will now be a weighted graph with the
        default weight of 1 for each edge.

        """
        
        self.weighted = True # slightly evil hack. works fine because
                             # all graphs are stored internally as
                             # weighted graphs.

    def convertToDirected(self):
        """Convert the current graph to a directed graph.

        If the graph is already directed, it will be unchanged. If it
        is undirected, it will now be an equivalent directed graph
        constructed by replacing each undirected edge with two
        directed edges between the same nodes, one in each direction.

        """
        
        self.directed = True # slightly evil hack. works fine because
                             # all graphs are stored internally as
                             # directed graphs.

    def pathLength(self, path):
        """Return the "length" of the given path (i.e. total weight of its edges)

        For unweighted graphs, the length of the path is the number of
        edges in it. For weighted graphs, the "length" is the total
        weight of its edges. If the given path is not in fact a path
        in the current graph, an exception is raised.

        Args:

            path (Path): the sequence p of nodes to be investigated

        Returns:

            int: the total weight of the edges in the path

        """
        if not self.isPath(path):
            raise WcbcException(str(path) + ' is not a path in the graph ' + str(self))
        length = 0
        for edge in path:
            length += self.getWeight(edge)
        return length
        

    def cycleLength(self, cycle):
        """Return the "length" of the given cycle (i.e. total weight of its edges)

        For unweighted graphs, the length of the cycle is the number of
        edges in it. For weighted graphs, the "length" is the total
        weight of its edges. If the given cycle is not in fact a cycle
        in the current graph, an exception is raised.

        See the important note in the documentation for isCycle(): the
        given cycle parameter should not explicitly contain the final
        edge back to the start of the cycle; it will be added
        implicitly.

        Args:

            cycle (Path): the sequence p of nodes to be investigated

        Returns:

            int: the total weight of the edges in the cycle

        """
        if not self.isCycle(cycle):
            raise WcbcException(str(cycle) + ' is not a cycle in the graph ' + str(self))
        if len(cycle)==0:
            return 0
        pathLen = self.pathLength(cycle)
        finalEdge = Edge([cycle.end(), cycle.start()])
        return pathLen + self.getWeight(finalEdge)

    def chooseNode(self):
        """Return an arbitrary node in the current graph

        Returns:

            str: an arbitrary node in the current graph, or None if
            the graph contains no nodes.

        """

        # use a for loop to choose the "first" node in the dictionary
        # of nodes...
        for node in self.nodes:
            return node
        # ...or None if no nodes
        return None

    def sumEdgeWeights(self):
        """Return the total weight of all edges in the graph.

        For unweighted graphs, each edge has an implicit weight of 1.

        Returns:

            int: the total weight of all edges in the graph.

        """

        total = 0
        for edge in self.edges():
            total += self.getWeight(edge)
        return total


##############################
## see graphTest.py for tests
##############################


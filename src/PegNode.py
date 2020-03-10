class PegNodeLink:
    '''PegNodeLink objects provide mapping of legal jumps from a PegNode
    
    When jumping, a PegNodeLink provides the start_node that a peg is currently located at, an adjacent_node that can be jumped over (if a peg is at that location), and an end_node (which must be empty) for the peg to land at after jumping.
    
    Arguments:
      start_node(PegNode): Beginning Node Position
      adjacent_node(PegNode): Adjacent Node that will be jumped over
      end_node(PegNode): Ending Node that will be jumped to
    '''
    def __init__(self, start_node, adjacent_node, end_node):
        if isinstance(start_node, PegNode):
            self._start_node = start_node
        else:
            ValueError('start_node must be a PegNode instance')
        if isinstance(adjacent_node, PegNode):
            self._adjacent_node = adjacent_node
        else:
            ValueError('adjacent_node must be a PegNode instance')
        if isinstance(end_node, PegNode):
            self._end_node = end_node
        else:
            ValueError('end_node must be a PegNode instance')
            
    def __str__(self):
        return '{}->{}->{}'.format(self._start_node, self._adjacent_node, self._end_node)

class PegNode:
    '''Create a new PegNode instance
    
    Arguments:
      parent: the parent that owns this node, a dict with {node_id: node} entries
      node_id: a unique key that identifies this PegNode
      node_id_str: a string that will be printed out for the node_id. This will be created from the default __str__() of the node_id if not provided
    '''
    def __init__(self, parent, node_id, node_id_str=''):
        self._node_id = node_id
        if node_id_str:
            self._node_id_str = node_id_str
        else:
            self._node_id_str = str(node_id_str)
        self._parent = parent
        self._links = []
    
    def node_id(self):
        return self._node_id
    
    def add_link(self, adjacent_node, end_node):
        self._links.append(PegNodeLink(self, adjacent_node, end_node))
        
    def __str__(self):
        return '{}'.format(self._node_id_str) 
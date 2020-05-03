class PegNodeLink:
    '''PegNodeLink objects provide mapping of legal jumps from a PegNode
    
    When jumping, a PegNodeLink provides the start_node that a peg is currently located at, an adjacent_node that can be jumped over (if a peg is at that location), and an end_node (which must be empty) for the peg to land at after jumping.
    
    Arguments:
      start_node(PegNode): Beginning Node Position
      adjacent_node(PegNode): Adjacent Node that will be jumped over
      end_node(PegNode): Ending Node that will be jumped to
    '''

    def __init__(self, start_node, adjacent_node, end_node):
        from .PegNode import PegNode

        if isinstance(start_node, PegNode):
            self._start_node = start_node
        else:
            raise ValueError('start_node must be a PegNode instance')
        if isinstance(adjacent_node, PegNode):
            self._adjacent_node = adjacent_node
        else:
            raise ValueError('adjacent_node must be a PegNode instance')
        if isinstance(end_node, PegNode):
            self._end_node = end_node
        else:
            raise ValueError('end_node must be a PegNode instance')

    def start_node(self):
        return self._start_node

    def adjacent_node(self):
        return self._adjacent_node

    def end_node(self):
        return self._end_node

    def __str__(self):
        return '{}->{}->{}'.format(self._start_node.node_id_str(), self._adjacent_node.node_id_str(), self._end_node.node_id_str())

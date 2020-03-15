try:
    from .PegNodeLink import PegNodeLink
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))

class PegNodeException(Exception):
    pass

class PegNode:
    '''Create a new PegNode instance
    
    Arguments:
      parent: the parent that owns this node, a dict with {node_id: node} entries
      node_id: a unique key that identifies this PegNode
      node_id_str {str}: a string that will be printed out for the node_id. This will be created from the default __str__() of the node_id if not provided
    '''
    def __init__(self, node_id, node_id_str='', peg=False):
        self._node_id = node_id
        if node_id_str:
            self._node_id_str = node_id_str
        else:
            self._node_id_str = str(node_id)
        if not isinstance(self._node_id_str, str):
            raise ValueError('"node_id_str" (arg 3) must be a string, it was {}'.format(type(self._node_id_str)))
        self._parent = None
        self._links = []
        # If peg arg evaluates to anything, set to True, else False
        self._peg = True if peg else False
    
    def set_parent(self, parent):
        if self._parent == None:
            self._parent = parent
        else:
            raise PegNodeException('for node(node_id={}), parent has already been set!!'.format(self.node_id()))
        
    def parent(self):
        return self._parent
    
    def peg(self):
        return self._peg
    
    def peg_str(self):
        return 'x' if self._peg else 'o'
    
    def set_peg(self, peg_value):
        self._peg = True if peg_value else False
    
    def add_peg(self):
        if self._peg:
            raise ValueError('Peg already present at Node {}, cannot add'.format(self.node_id()))
        else:
            self._peg = True
    
    def remove_peg(self):
        if self._peg:
            self._peg = False
        else:
            raise ValueError('No peg was present at Node {} to remove'.format(self.node_id()))
    
    def node_id(self):
        return self._node_id
    
    def node_id_str(self):
        return self._node_id_str
    
    def links(self):
        return self._links
    
    def add_link(self, adjacent_node, end_node):
        self._links.append(PegNodeLink(self, adjacent_node, end_node))
        
    def __str__(self):
        outstr = ('Node ID: {} (Type: {})\n'
                'Node ID String: "{}"\n'
                'Links:\n'.format(self._node_id, type(self._node_id), self._node_id_str))
        if self.links():
            for index, link in enumerate(self.links()):
                outstr += '  #{}: {}\n'.format(index, link)
        else:
            outstr += '  None\n'
        return outstr[:-1] # Strip last '\n'
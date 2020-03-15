try:
    from .PegNode import PegNode
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))
    
class PegException(Exception):
    pass

class PegBoard:
    '''class PegBoard is a linked list of nodes on a Peg Board
    
    PegBoard includes a list of nodes or positions on the current game board that includes tracking of legal moves between nodes (links), traversing of parent/child relationships, tracking of game pieces at a given node, etc.
    '''
    def __init__(self, nodelist):
        # Ensure nodes is a list of PegNodes
        if not isinstance(nodelist, list):
            raise ValueError('nodes argument was type "{}", expected "list"'.format(type(nodelist)))
        # Ensure every item is the list is a PegNode
        nodes_are_not_PegNode = [type(node) != PegNode for node in nodelist]
        if any(nodes_are_not_PegNode):
            raise ValueError('{} of {} items in nodes argument are not type PegNode'.format(sum(nodes_are_not_PegNode), len(nodelist)))
        
        ## create the nodes list
        self._nodes = {}
        newnodes = { node.node_id(): node for node in nodelist }
        self._nodes.update(newnodes)
        self._node_ids = [ node_id for node_id in self._nodes.keys() ]
        for node in self.nodes():
            node.set_parent(self)

        # Setup _format_str to None so it is initialized,
        # need child class to set this up!!
        self._format_str = None

    def node_ids(self):
        return self._node_ids

    def node_ids_str(self):
        try: # If not set yet, we will lazy-load
            return self._node_ids_str
        except AttributeError:
            self._node_ids_str = [ node.node_id_str() for node in self.nodes() ]
            return self._node_ids_str
            
    def nodes(self):
        return self._nodes.values()

    def node(self, node_id):
        return self._nodes[node_id]

    def pegs(self):
        """return a dict of node_id: peg_value for each node
        """
        return { node.node_id(): node.peg() for node in self.nodes() }

    def set_pegs(self, pegs):
        """set the peg value of a node (whether peg is present or not)
        
        Different from .add_peg() in that no error if there is already a peg present. Different from .remove_peg() in that no error if there is no peg to remove. It just sets the raw value.
        
        Arguments:
            pegs {dict} -- each key is a node_id, value is the peg value to set for the corresponding node. If a node_id is not present, that node will not have its peg property altered.
            pegs {bool, int} -- When not a list, will assign whatever boolean value that pegs evaluates to as the pegs value of every node (all set to False or True)
        """
        if isinstance(pegs, dict):
            for node_id, peg_value_to_set in pegs.items():
                self.node(node_id).set_peg(peg_value_to_set)
        elif isinstance(pegs, (int, bool)):
            # apply the value to every node (assume a single value that evaluates to Boolean)
            peg_value_to_set = bool(pegs)
            for node in self.nodes():
                node.set_peg(peg_value_to_set)
        else:
            raise ValueError('Argument Pegs was type <{}>, expected dict, bool, or int'.format(type(pegs)))
  
    def count_pegs(self):
        """Return the number of pegs currently in nodes on this board
        """
        return sum([ node.peg() for node in self.nodes()])

    ## Format Strings and functions for printing Board status and other info strings.
    # Note: Format string is set by the user/child class, the PegBoard class just fills in the information from the class object (i.e. filling in node ids, peg positions, etc.)
    def format_str(self):
        if self._format_str == None:
            raise ValueError('Child Class must create _format_str variable!!')
        return self._format_str

    def nodes_str(self, indent=0):
        outstr = self.format_str().format(x=self.node_ids_str())
        return self._indent_string(outstr, indent)
    
    def pegs_str(self, indent=0):
        pegs = [ node.peg_str() for node in self.nodes() ]
        outstr = self.format_str().format(x=pegs)
        return self._indent_string(outstr, indent)
    
    def full_str(self, indent=0):
        fullstr = [ '{}:{}'.format(node.node_id_str(), node.peg_str()) for node in self.nodes() ]
        outstr = self.format_str().format(x=fullstr)
        spaces = ' ' * 3
        outstr = outstr.replace(' ', spaces)
        return self._indent_string(outstr, indent)
    
    def node_and_pegs_str(self, indent=0, space_between=3):
        node = self.nodes_str()
        pegs = self.pegs_str()
        nodelines = node.splitlines()
        peglines = pegs.splitlines()
        outstr = '\n'.join([ '{}{}{}'.format(nodelines[index], ' ' * space_between, peglines[index]) for index, _ in enumerate(nodelines) ])
        return self._indent_string(outstr, indent)
    
    def _indent_string(self, text, indent):
        spaces = ' ' * indent
        outstr = ''.join([spaces + row + '\n' for row in text.splitlines()])
        return outstr[:-1]

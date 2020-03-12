try:
    from .PegNode import PegNode
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))
    
class PegException(Exception):
    pass

class PegBoard:
    '''PegBoard is a linked list of nodes on a Peg Board
    
    PegBoard includes information on the board geometry of each
    individual node where a peg can be, in addition to information
    about how moves can happen (i.e. which nodes are adjacent,
    and where a jump over that adjacent node will land)
    
    Arguments:
       node_ids as list:
          list of ids to use for each node that is created
       [node_ids_str] as list:
          list of id strings that matchs the node_ids. These will be returned when attempting to print a node. If left off or empty, the built-in string function for each id will be used instead.  
    '''
    def __init__(self, node_ids, node_ids_str=None):
        # Ensure node_ids is a list
        if not isinstance(node_ids, list):
            raise ValueError('node_ids (arg 1) was type "{}", expected "list"'.format(type(node_ids)))
        
        # If not provided, set node_ids_str to a list of the default string output of the node_ids list items
        if node_ids_str == None:
            node_ids_str = [str(x) for x in node_ids]
        else:
            # if node_ids_str was given, check that it is a list
            if not isinstance(node_ids_str, list):
                raise ValueError('node_ids_str (arg 2) was type "{}", expected "list"'.format(type(node_ids)))
            # if it is a list, check if all items are strings
            if not all(isinstance(x, str) for x in node_ids_str):
                raise ValueError('if provided, all items in Arg 3, node_ids_str, "{}" list must be strings'.format(node_ids_str))
        
        # Ensure input args are the same length as lists
        if len(node_ids) != len(node_ids_str):
            raise ValueError('Length of node_ids (arg 1) [{}] does not equal length of node_ids_str (arg 2) [{}]'.format(len(node_ids), len(node_ids_str)))
        
        ## create the nodes list
        nodes = {}
        newnodes = {node_id: PegNode(nodes, node_id, node_ids_str[index]) for index, node_id in enumerate(node_ids)}
        nodes.update(newnodes)

        ## Assign all object properties        
        self._node_ids = node_ids
        self._node_ids_str = node_ids_str
        self._nodes = nodes
        
        # Setup _format_str to None so it is initialized,
        # need child class to set this up!!
        self._format_str = None
        
    def node(self, node_id):
        return self._nodes[node_id]
    
    def nodes(self):
        return self._nodes

    ## Format Strings and functions for printing Board status and other info strings.
    # Note: Format string is set by the user/child class, the PegBoard class just fills in the information from the class object (i.e. filling in node ids, peg positions, etc.)
    def format_str(self):
        if self._format_str == None:
            raise ValueError('Child Class must create _format_str variable!!')
        return self._format_str

    def nodes_str(self, indent=0):
        outstr = self.format_str().format(x=self._node_ids_str)
        return self._indent_string(outstr, indent)
    
    def pegs_str(self, indent=0):
        pegs = [ self.node(node_id).peg_str() for node_id in self._node_ids ]
        outstr = self.format_str().format(x=pegs)
        return self._indent_string(outstr, indent)
    
    def full_str(self, indent=0):
        fullstr = [ '{}:{}'.format(self._nodes[node_id].node_id_str(), self._nodes[node_id].peg_str()) for node_id in self._node_ids ]
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
        outstr = ''.join([spaces + line + '\n' for line in text.splitlines()])
        return outstr[:-1]

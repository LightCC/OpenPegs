try:
    from .PegNode import PegNode
    from .PegBoard import PegBoard
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))
    
class PegException(Exception):
    pass

class PegBoard:
    def __init__(self, nodes, node_ids, node_ids_str=None):
        # If not provided, set node_ids_str to a list of the default string output of the node_ids list items
        if node_ids_str == None:
            node_ids_str = [str(x) for x in node_ids]
        else:
            if not all(isinstance(x, str) for x in node_ids_str):
                raise ValueError('if provided, all items in Arg 3, node_ids_str, "{}" list must be strings'.format(node_ids_str))

        # Check all args for list type and equal lengths
        args = [nodes, node_ids, node_ids_str]
        argsstr = ['nodes', 'node_ids', 'node_ids_str']
        required_type = [dict, list, list]
        for index, arg in enumerate(args):
            if not isinstance(arg, required_type[index]):
                raise ValueError('Arg {} of {}: "{}" must be a "{}" type'.format(index + 1, len(args), argsstr[index], required_type[index]))
            if len(nodes) != len(arg):
                raise ValueError('Arg {} of {}: "{}" has length of {} instead of length of arg 1, the nodes list ({})'.format(index + 1, len(args), arg, len(arg), len(nodes)))
        self._node_ids = node_ids
        self._node_ids_str = node_ids_str
        self._nodes = nodes
        
        # Setup _format_str to None so it is initialized,
        # but need child class to handle these
        self._format_str = None
        
    def node(self, node_id):
        return self._nodes[node_id]
        
    def nodes(self):
        return self._nodes

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
    
    def node_and_pegs_str(self, indent=0):
        node = self.nodes_str()
        pegs = self.pegs_str()
        nodelines = node.splitlines()
        peglines = pegs.splitlines()
        outstr = '\n'.join([ '{} {}'.format(nodelines[index], peglines[index]) for index, _ in enumerate(nodelines) ])
        return self._indent_string(outstr, indent)
    
    def _indent_string(self, text, indent):
        spaces = ' ' * indent
        outstr = ''.join([spaces + line + '\n' for line in text.splitlines()])
        return outstr[:-1]
    
    def format_str(self):
        if self._format_str == None:
            raise ValueError('Child Class must create _format_str variable!!')
        return self._format_str

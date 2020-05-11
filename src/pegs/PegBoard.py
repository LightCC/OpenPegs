from typing import Dict, List, Tuple
from .PegException import *


class PegBoard:
    '''class PegBoard is a linked list of nodes on a Peg Board
    
    PegBoard includes a list of nodes or positions on the current game board that includes tracking of legal moves between nodes (links), traversing of parent/child relationships, tracking of game pieces at a given node, etc.
    '''

    @staticmethod
    def _indent_string(text, indent):
        spaces = ' ' * indent
        outstr = ''.join([spaces + row + '\n' for row in text.splitlines()])
        return outstr[:-1]

    @classmethod
    def _create_format_str(cls, nodes, rows):
        """Create the format string for a generic game board, that is used to print the game board

        Args:
            nodes (Dict[int,str]): Dict of nodes, keys are integer ids, values are id strings
            rows (List[List,int]): List of rows, each is a list of Node IDs in that row

        Returns:
            str: The format string with "{{x[node]}}" in place of each node, where it will be shown in a printout using other functions like nodes_string, pegs_string, full_string, etc.
        """
        ## Create a dict of rows with their lengths
        row_lengths = [len(row) for row in rows]
        max_nodes_in_row = max(row_lengths)
        ## Now create a string for each row and combine them
        rows_str = []
        for row in rows:
            # Center each row by adding spaces
            row_center_spacing = ' ' * (max_nodes_in_row - len(row))
            rowstr = row_center_spacing
            node_index = {node: index for index, node in enumerate(nodes)}
            for node in row:
                rowstr += '{{x[{node_index}]}} '.format(node_index=node_index[node])
            rowstr += row_center_spacing
            # rowstr will have one extra space at the end from the loop, strip one off
            rows_str.append(rowstr[:-1])
            # Remove the final '\n' from outstr
        return '\n'.join(rows_str)

    def __init__(self, nodes: Dict[int, str], format_str: str):
        """Initialize a PegBoard

        Args:
            nodes (Dict[int, str]): a dict of node ids (int) and their associated strings when printing the node as a string
            links (List[Tuple[int, int, int]]): a list of all legal node connections, jumping from one node, over another, onto a third
            format_str (str): Format Strings for printing Board status and other info strings. A physical layout of the board with "{{x[node]}}" in the string where each node position is represented (replace "node" with the node id)
        """

        self._nodes_str: Dict[int, str] = nodes
        self.nodes: List[int] = [node for node in nodes]
        self._pegs: Dict[int, bool] = {node: False for node in nodes}
        self.format_str: str = format_str

    def node_str(self, node: int) -> str:
        return self._nodes_str[node]

    def node_from_node_str(self, node_str) -> int:
        """Returns the node id associated with a given node id string.
        
        Args:
            node_str (str): a node string that corresponds to a game board node
            
        Returns:
            node (int): the node that has the id_str
        """
        for node, id_str in self._nodes_str.items():
            if id_str == node_str:
                return node
        raise PegNodeException('{} not found in node strings'.format(node_str))

    @property
    def pegs(self):
        """return a dict of {node_id: PegNodePeg object} for each node
        """
        return self._pegs

    @pegs.setter
    def pegs(self, pegs):
        """set the peg value of a node (whether peg is present or not)
        
        Different from .add_peg() in that no error if there is already a peg present. Different from .remove_peg() in that no error if there is no peg to remove. It just sets the raw value.
        
        Args:
            pegs {dict} -- each key is a node_id, value is the peg value to set for the corresponding node. If a node_id is not present, that node will not have its peg property altered.
            pegs {bool, int} -- When not a list, will assign whatever boolean value that pegs evaluates to as the pegs value of every node (all set to False or True)
        """
        if isinstance(pegs, dict):
            for node, peg_is_present in pegs.items():
                self._pegs[node] = peg_is_present
        elif isinstance(pegs, (int, bool)):
            # apply the value to every node (assume a single value that evaluates to Boolean)
            peg_is_present = bool(pegs)
            self._pegs = {node: peg_is_present for node in self._pegs}
        else:
            raise ValueError(f'Argument Pegs <{pegs}> was type <{type(pegs)}>, expected dict, bool, or int')

    def count_pegs(self):
        """Return the number of pegs currently in nodes on this board
        """
        return sum([peg for peg in self._pegs.values()])

    def peg(self, node: int):
        return self.pegs[node]

    def peg_str(self, node):
        return 'x' if self.peg(node) else 'o'

    def _set_peg(self, node: int, is_present: bool):
        self._pegs[node] = is_present

    def add_peg(self, node):
        if isinstance(node, str):
            node = self.node_from_node_str(node)
        if self.peg(node):
            raise PegAlreadyPresent(f'Peg already present at node "{self.node_str(node)}", cannot add')
        else:
            self._set_peg(node, True)

    def remove_peg(self, node):
        if not self.peg(node):
            raise PegNotAvailable(f'Peg not available at node "{self.node_str(node)}" to remove')
        else:
            self._set_peg(node, False)

    def nodes_string(self, indent=0):
        outstr = self.format_str.format(x=self._nodes_str)
        return self._indent_string(outstr, indent)

    def pegs_string(self, indent=0):
        pegs_str = [self.peg_str(node) for node in self.pegs]
        outstr = self.format_str.format(x=pegs_str)
        return self._indent_string(outstr, indent)

    def full_string(self, indent=0):
        fullstr = [f'{self.node_str(node)}:{self.peg_str(node)}' for node in self.nodes]
        outstr = self.format_str.format(x=fullstr)
        spaces = ' ' * 3
        outstr = outstr.replace(' ', spaces)
        return self._indent_string(outstr, indent)

    def node_and_pegs_string(self, indent=0, space_between=3):
        node = self.nodes_string()
        pegs = self.pegs_string()
        nodelines = node.splitlines()
        peglines = pegs.splitlines()
        spaces = ' ' * space_between
        outstr = '\n'.join([f'{nodes}{spaces}{pegs}' for nodes, pegs in zip(nodelines, peglines)])
        return self._indent_string(outstr, indent)

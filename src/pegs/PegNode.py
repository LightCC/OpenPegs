from typing import Any, List, Tuple

try:
    from .PegNodeLink import PegNodeLink
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))


class PegNodeException(Exception):
    pass


class PegNode:
    """The node of a game board, linked to other nodes, that can hold a peg.

    Arguments:
        node_id {Any} -- a unique, hashable, node id for this PegNode

    Keyword Arguments:
        node_id_str {str} -- string format of the node_id when  printing the board (default: {''})
        peg {bool} -- true when a peg is present in the PegNode (default: {False})

    Raises:
        ValueError: node_id_str is not a string
    """

    def __init__(self, node_id: Any, node_id_str: str = '', peg: bool = False) -> None:
        self._node_id = node_id
        if node_id_str:
            self._node_id_str = node_id_str
        else:
            self._node_id_str = str(node_id)
        if not isinstance(self._node_id_str, str):
            raise ValueError('"node_id_str" (arg 3) must be a string, it was {}'.format(type(self._node_id_str)))
        self._parent = None
        self._links: List[PegNodeLink] = []
        # If peg arg evaluates to anything, set to True, else False
        self._peg = True if peg else False

    def set_parent(self, parent: Any) -> None:
        """[summary]

        Args:
            parent (Any): [description]

        Raises:
            PegNodeException: [description]
        """
        if self._parent is None:
            self._parent = parent
        else:
            raise PegNodeException('for node(node_id={}), parent has already been set!!'.format(self.node_id()))

    def parent(self):
        return self._parent

    def peg(self):
        return self._peg

    def peg_str(self):
        return 'x' if self._peg else 'o'

    def set_peg(self, peg_value: bool) -> None:
        """Summarize something.

        :param peg_value: describe a thing
        """
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
        outstr = ('Node ID: {} (Type: {})\n' 'Node ID String: "{}"\n' 'Links:\n'.format(self._node_id, type(self._node_id), self._node_id_str))
        if self.links():
            for index, link in enumerate(self.links()):
                outstr += '  #{}: {}\n'.format(index, link)
        else:
            outstr += '  None\n'
        return outstr[:-1]     # Strip last '\n'

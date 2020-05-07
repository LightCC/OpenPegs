from typing import Any, List, Tuple
from collections.abc import Hashable
from .PegException import *

try:
    from .PegNodeLink import PegNodeLink
    from .PegNodePeg import PegNodePeg
    from .PegNodeId import PegNodeId
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))


class PegNode:
    """The node of a game board, linked to other nodes, that can hold a peg"""

    def __init__(self, node_id: int, id_str: str = None, peg_is_present: Any = False) -> None:
        """Initialize a new PegNode

        Args:
            node_id (Hashable): Hashable node id for this node
            node_id_str (str, optional): String that will print for this node. Defaults to built-in string output for the node_id.
            peg_is_preset (bool, optional): Whether a peg is present in the node. Defaults to False.

        Raises:
            ValueError: When node_id_str is not a string
        """
        self._node_id = PegNodeId(node_id, id_str=id_str)
        self._parent = None
        self.links: List[PegNodeLink] = []
        if isinstance(peg_is_present, PegNodePeg):
            raise ValueError("peg_is_preset must be a truthy type, not PegNodePeg")
        self._peg = PegNodePeg(peg_is_present)

    @property
    def node_id(self):
        return self._node_id.value

    @property
    def node_id_str(self):
        return str(self._node_id)

    @property
    def node_id_obj(self):
        return self._node_id

    @property
    def peg_is_present(self):
        return self._peg.peg

    @peg_is_present.setter
    def peg_is_present(self, peg_is_present):
        self._peg.peg = peg_is_present

    @property
    def peg_str(self):
        return str(self._peg)

    @property
    def peg_obj(self):
        return self._peg

    def add_peg(self):
        try:
            self._peg.add_peg()
        except PegAlreadyPresent as ex:
            raise PegAlreadyPresent('{}, at node {}'.format(ex, self.node_id))

    def remove_peg(self):
        try:
            self._peg.remove_peg()
        except PegNotAvailable as ex:
            raise PegNotAvailable('{}, at node {}'.format(ex, self.node_id))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: Any) -> None:
        ## FIXME docstring
        """[summary]

        Args:
            parent (Any): [description]

        Raises:
            PegNodeException: [description]
        """
        if self._parent is None:
            self._parent = parent
        else:
            raise PegNodeException('for node(node_id={}), parent has already been set!!'.format(self.node_id))

    def add_link(self, adjacent_node, end_node):
        self.links.append(PegNodeLink(self, adjacent_node, end_node))

    def __repr__(self):
        outstr = (  #
            'Node ID: {}\n'
            'Node ID String: "{}"\n'
            'Peg Status: {}'
            'Links:\n'  #
            .format(
                self.node_id.value,
                str(self.node_id),
                str(self._peg),
            )
        )
        if self.links:
            for index, link in enumerate(self.links):
                outstr += '  #{}: {}\n'.format(index, link)
        else:
            outstr += '  None\n'
        return outstr[:-1]  # Strip last '\n'

    def __str__(self):
        return self.node_id_str
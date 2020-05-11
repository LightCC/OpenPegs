from typing import Any, List, Tuple
from .PegNodeId import PegNodeId
from .PegException import *
from .PegNodeLink import PegNodeLink
from .PegNodePeg import PegNodePeg


class PegNode:
    """The node of a game board, linked to other nodes, that can hold a peg"""

    def __init__(self, node_id: int) -> None:
        """Initialize a new PegNode

        Args:
            node_id (int): Node id for this node

        Raises:
            ValueError: When node_id_str is not a string
        """
        self._node_id = node_id

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
    def peg_object(self):
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

    def __eq__(self, other):
        if not all(
                self.node_id == other.node_id,
                self.node_id_str == other.node_id_str,
                self.peg_is_present == other.peg_is_present,
                id(self.parent) == id(other.parent),
        ):
            return False
        for link1, link2 in zip(self.links, other.links):
            if not link1.link_id == link2.link_id:
                return False
        return True

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
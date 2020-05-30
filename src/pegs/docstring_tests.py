from typing import Any, List
from typing import Tuple


class AutoDocTest:

    def autodoc_test_google(self, a: str, b: int = 5, c: Tuple[int, int] = (1, 2)) -> Any:
        """[summary]

        Args:
            a (str): [description]
            b (int, optional): [description]. Defaults to 5.
            c (Tuple[int, int], optional): [description]. Defaults to (1, 2).

        Raises:
            ValueError: [description]

        Returns:
            Any: [description]
        """
        a1 = 1*2 + 3/4 + 1 + 2 * 5 / int(a)
        b2 = 2*5 + 2/2*b
        if a is None:
            raise ValueError("A test exception")
        return b2

    def autodoc_test_sphinx(self, a: str, b: int, c: Tuple[int, int] = (1, 2)) -> Any:
        """[summary]

        :param a: [description]
        :type a: str
        :param b: [description], defaults to 5
        :type b: int, optional
        :param c: [description], defaults to (1, 2)
        :type c: Tuple[int, int], optional
        :raises ValueError: [description]
        :return: [description]
        :rtype: Any
        """
        a1 = 1*2 + 3/4 + 1 + 2 * 5 / int(a)
        b2 = 2*5 + 2/2*b
        if a is None:
            raise ValueError("A test exception")
        return b2

    def autodoc_test_numpy(
        self,
        a: str,
        b: int = 5,
        c: Tuple[int, int] = (1, 2),
    ) -> Any:
        """[summary]

        ### Parameters
        1. a : str
            - [description]
        2. *b : int, (default 5)
            - [description]
        3. *c : Tuple[int, int], (default (1, 2))
            - [description]

        ### Returns
        - Any
            - [description]

        Raises
        ------
        - ValueError
            - [description]
        """
        a1 = 1*2 + 3/4 + 1 + 2 * 5 / int(a)
        b2 = 2*5 + 2/2*b
        if a is None:
            raise ValueError("A test exception")
        return b2

    def doctest_argument_comments(
        self,
        a: Any,  # description of a
        b: int = 5,  # description of b
    ) -> List[int]:  # description of return value
        """[summary]

        Args:
            a (Any): [description]

        Raises:
            ValueError: [description]

        Returns:
            List[int]: [description]
        """
        raise ValueError("A test exception")


class MyDocStringTestClase:
    """Google Format: The node of a game board, linked to other nodes, that can
    hold a peg.

    Arguments:
        node_id {Any} -- a unique, hashable, node id for this PegNode

    Keyword Arguments:
        id_str {str} -- string format of the node_id when  printing the board (default: {''})
        peg {bool} -- true when a peg is present in the PegNode (default: {False})

    Raises:
        ValueError: id_str is not a string
    """
    """Sphinx: [summary]

    :param node_id: [description]
    :type node_id: Any
    :param id_str: [description], defaults to ''
    :type id_str: str, optional
    :param peg: [description], defaults to False
    :type peg: bool, optional
    :raises ValueError: [description]
    :return: [description]
    :rtype: [type]
    """
    """NumPY: PegNode summary

    Parameters
    ----------
    node_id : Hashable
        a description of node id
    id_str : str, optional
        desc of id_str, by default ''
    peg : bool, optional
        desc of peg, by default False

    Raises
    ------
    ValueError
        [description]
    """

    def __init__(self, node_id: Any, id_str: str = '', peg: bool = False) -> None:
        a = (node_id, id_str, peg)
        if node_id is None:
            raise ValueError('must supply node_id')

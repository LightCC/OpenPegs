from typing import List, NamedTuple
from .PegBoard import PegBoard
from .PegNodeLink import PegNodeLink
from collections import namedtuple


class PegPyramid(PegBoard):

    class State(NamedTuple):
        peg_0: int = False
        peg_1: int = False
        peg_2: int = False
        peg_3: int = False
        peg_4: int = False
        peg_5: int = False
        peg_6: int = False
        peg_7: int = False
        peg_8: int = False
        peg_9: int = False
        peg_10: int = False
        peg_11: int = False
        peg_12: int = False
        peg_13: int = False
        peg_14: int = False

        @property
        def count(self):
            return sum(self)
            
        def __repr__(self):
            outstr = ('PegPyramid.State(' + ', '.join([f'{fld}={val}' for fld, val in zip(self._fields, self)]) + ')')  # pylint: disable=no-member
            return outstr

    NODES = {
        0: '0',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: 'a',
        11: 'b',
        12: 'c',
        13: 'd',
        14: 'e',
    }
    LINKS = {
        0: [
            PegNodeLink(0, 2, 5),
            PegNodeLink(0, 1, 3),
            PegNodeLink(0, 2, 5),
        ],
        1: [
            PegNodeLink(1, 3, 6),
            PegNodeLink(1, 4, 8),
        ],
        2: [
            PegNodeLink(2, 4, 7),
            PegNodeLink(2, 5, 9),
        ],
        3: [
            PegNodeLink(3, 1, 0),
            PegNodeLink(3, 4, 5),
            PegNodeLink(3, 6, 10),
            PegNodeLink(3, 7, 12),
        ],
        4: [
            PegNodeLink(4, 7, 11),
            PegNodeLink(4, 8, 13),
        ],
        5: [
            PegNodeLink(5, 2, 0),
            PegNodeLink(5, 4, 3),
            PegNodeLink(5, 8, 12),
            PegNodeLink(5, 9, 14),
        ],
        6: [
            PegNodeLink(6, 3, 1),
            PegNodeLink(6, 7, 8),
        ],
        7: [
            PegNodeLink(7, 4, 2),
            PegNodeLink(7, 8, 9),
        ],
        8: [
            PegNodeLink(8, 4, 1),
            PegNodeLink(8, 7, 6),
        ],
        9: [
            PegNodeLink(9, 5, 2),
            PegNodeLink(9, 8, 7),
        ],
        10: [
            PegNodeLink(10, 6, 3),
            PegNodeLink(10, 11, 12),
        ],
        11: [
            PegNodeLink(11, 7, 4),
            PegNodeLink(11, 12, 13),
        ],
        12: [
            PegNodeLink(12, 7, 3),
            PegNodeLink(12, 8, 5),
            PegNodeLink(12, 11, 10),
            PegNodeLink(12, 13, 14),
        ],
        13: [
            PegNodeLink(13, 8, 4),
            PegNodeLink(13, 12, 11),
        ],
        14: [
            PegNodeLink(14, 9, 5),
            PegNodeLink(14, 13, 12),
        ],
    }
    ROWS = [
        [0],
        [1, 2],
        [3, 4, 5],
        [6, 7, 8, 9],
        [10, 11, 12, 13, 14],
    ]
    _FORMAT_STR = (  #
        '    {x[0]}    \n'
        '   {x[1]} {x[2]}   \n'
        '  {x[3]} {x[4]} {x[5]}  \n'
        ' {x[6]} {x[7]} {x[8]} {x[9]} \n'
        '{x[10]} {x[11]} {x[12]} {x[13]} {x[14]}'
    )

    def __init__(self, initial_node: int = None, board_id: State = None):
        PegBoard.__init__(self, self.NODES, self._FORMAT_STR)
        if initial_node is not None:
            if not isinstance(initial_node, int):
                raise ValueError(f'initial_node ({initial_node}) must be an integer (was {type(initial_node)}')
            self.setup_game_board_from_initial_node(initial_node)
        elif board_id:
            if not isinstance(board_id, self.State):
                raise ValueError(f'board_id type must be State(NamedTuple), was {type(board_id)}')
            self.board_id = board_id
            self._valid_moves = self._find_valid_moves()
        else:
            self._valid_moves = None

    def __str__(self):
        return self.pegs_string()

    def __eq__(self, other):
        if not isinstance(self, PegPyramid) or not isinstance(other, PegPyramid):
            return NotImplemented
        return self.board_id == other.board_id

    def setup_game_board_from_initial_node(self, start_node) -> None:
        """Adds pegs to all positions except the given starting node
        
        Args:
            start_node (int, str): the starting node on the game board as either a node_id or the string of a node_id
        Raises:
            AttributeError: start_node is not a node in this game board
        """
        if isinstance(start_node, str):
            start_node = self.node_from_node_str(start_node)
        if start_node in self.NODES:
            for node in self.NODES:
                peg = not (start_node == node)
                self._set_peg(node, peg)
            self._valid_moves = self._find_valid_moves()
        else:
            raise AttributeError("{} is not a node in the GameBoard")

    @property
    def valid_moves(self):
        if self._valid_moves is None:
            self._valid_moves = self._find_valid_moves()
        return self._valid_moves

    def _find_valid_moves(self):
        ## TODO: Optimize this - its a very rough brute force calculation...
        moves = []
        for node in self.NODES:
            for link in self.LINKS[node]:
                if self.link_has_valid_jump(link):
                    moves.append(link)
        return moves

    def link_has_valid_jump(self, link):
        # If start node has a peg, and adjacent node has a peg to jump, and end node is empty to land, then link is valid for a jump
        return all([
            self.peg(link.start),
            self.peg(link.adjacent),
            not self.peg(link.end),
        ])

    def execute_jump_move(self, link):
        if self.link_has_valid_jump(link):
            self.remove_peg(link.adjacent)  # Jump over here and remove peg from board
            self.remove_peg(link.start)  # Jump from here, peg moves
            self.add_peg(link.end)  # peg lands here and fills the spot
            self._valid_moves = self._find_valid_moves()
        else:
            if not self.peg(link.start):
                raise ValueError(f'Link {link} is not valid - No peg to jump with in start node {link.start}')
            if not self.peg(link.adjacent):
                raise ValueError(f'Link {link} is not valid - No peg to jump over in adjacent node {link.adjacent}')
            if self.peg(link.end):
                raise ValueError(f'Link {link} is not valid - Peg already present in end node {link.end}')

    @property
    def board_id(self):
        """board_id provides a unique id for this board based on the current game board status
        
        board_id can be used to recreate the current board state, as a shorthand way of saving the board status, or determining if this board_state is already in the analysis database
        """
        board_id = self.State(*[self.peg(node) for node in self.pegs])
        return board_id

    @board_id.setter
    def board_id(self, value):
        if not isinstance(value, self.State):
            raise ValueError(f"board_id must be a State(NamedTuple), (was {type(value)})")
        for node, peg in zip(self.NODES, value):
            self._set_peg(node, peg)

    def analyze_current_game_board(self) -> List[PegNodeLink]:
        valid_moves: List[PegNodeLink] = []
        # TODO: Need to make a copy of the board, and actually complete the moves on it to find the full path.

        # TODO: this will only work for a board that only has one move left...
        if self.count_pegs() == 2:
            return self.valid_moves
        else:
            ## return an empty list if we couldn't analyze the board
            return []

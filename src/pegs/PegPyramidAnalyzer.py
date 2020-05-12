from typing import Dict, Any, Set
from .PegPyramid import PegPyramid
from .PegBoard import PegBoard
from .PegNodeLink import PegNodeLink


class PegPyramidAnalyzer:
    """Analyze future moves and build a database of possible moves and solutions for current game boards of PegPyramids
    """
    _board_moves = None

    def __init__(self) -> None:
        if self._board_moves is None:
            self._board_moves = {}
        self.test = PegPyramid()

    def analyze_game_board(self, board_id: PegPyramid.State) -> Any:
        moves = self.get_current_board_moves(board_id)
        return moves

    def get_current_board_moves(self, board_id):
        ## TODO
        peg_count = self.test.count_pegs()
        try:
            current_pegs_dict = self._board_moves[peg_count]
        except KeyError:  # haven't analyzed anything with that number of pegs yet
            current_pegs_dict = {}
        if board_id in current_pegs_dict:
            return current_pegs_dict[board_id]
        else:
            moves = self.test.valid_moves
        for move in moves:
            pass

    def get_board_from_move(self, board_id: PegPyramid.State, link: PegNodeLink) -> PegPyramid.State:
        if self.move_is_valid(board_id, link):
            pegs = [peg for peg in board_id]
            pegs[link.start] = False
            pegs[link.adjacent] = False
            pegs[link.end] = True
            return PegPyramid.State(*pegs)
        else:
            raise ValueError(f'link {link} is not valid in board, {board_id}')

    def find_valid_moves(self, board_id) -> Set[PegNodeLink]:
        moves = set()
        for node, peg in enumerate(board_id):
            for link in self.test.LINKS[node]:
                if self.move_is_valid(board_id, link):
                    moves.add(link)
        return moves

    def move_is_valid(self, board_id, link) -> bool:
        return all([
            board_id[link.start],
            board_id[link.adjacent],
            not board_id[link.end],
        ])

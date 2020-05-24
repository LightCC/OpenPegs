import dataclasses as dc
import typing as t
from .PegPyramid import PegPyramid, PyramidId
from .PegBoard import PegBoard
from .PegNodeLink import PegNodeLink


@dc.dataclass
class PegMove:
    link: PegNodeLink = None
    idx: PyramidId = PyramidId.make('ooooooooooooooo')


@dc.dataclass
class MoveChain:
    chain: t.List[PegMove] = None

    def add_chain(self, move: PegMove):
        if self.chain is None:
            self.chain = [move]
        else:
            self.chain.append(move)  # pylint: disable=no-member


class PegPyramidAnalyzer:
    """Analyze future moves and build a database of possible moves and solutions for current game boards of PegPyramids
    """
    _board_moves_db = None
    _move_chains_db = None

    def __init__(self) -> None:
        if self._board_moves_db is None:
            self._board_moves_db = {}
        if self._move_chains_db is None:
            self._move_chains_db = []
        self.test = PegPyramid()

    @property
    def move_count_in_board_db(self):
        total_moves = 0
        for boards_dict in self._board_moves_db.values():
            for moves in boards_dict.values():
                total_moves += len(moves)
        return total_moves

    @property
    def board_moves_db(self):
        return self._board_moves_db

    @property
    def move_chains_db(self):
        return self._move_chains_db

    def analyze_game_board(self, board_id: PyramidId) -> t.Any:
        raise NotImplementedError

    def find_move_chains(self, end_board_id: PyramidId = None, remaining_pegs: int = None) -> t.List[MoveChain]:
        if end_board_id:
            chains: t.Tuple[int, MoveChain] = [(index, chain) for index, chain in enumerate(self.move_chains_db) if chain.chain[-1].idx == end_board_id]
        elif remaining_pegs:
            chains = []
        else:
            ValueError('Must specify at least one optional argument as a search criteria')
        return chains

    def get_all_move_chains(self, board_id: PyramidId):
        start_chain = MoveChain(chain=[PegMove(idx=board_id)])
        self.recurse_next_board_chains(start_chain)

    def recurse_next_board_chains(self, start_chain: MoveChain, _recursion: int = 0) -> t.List[MoveChain]:
        if _recursion > 14:
            raise RecursionError('Too many levels!')
        last_board = start_chain.chain[-1].idx
        moves = self.get_current_board_moves(last_board)
        if moves:
            for link, board_id in moves.items():
                start_chain.add_chain(PegMove(link, board_id))
                # recurse to the next level for this move chain
                self.recurse_next_board_chains(start_chain, _recursion=_recursion + 1)
        else:
            # If no move, this is the final chain in recursion, so append it to the object move_chain_db
            peg_count = start_chain.chain[-1].idx.count
            self._move_chains_db.append(start_chain)

    def get_all_indiv_board_moves(self, board_id: PyramidId, _recursion=0) -> t.Any:
        """Generate all possible future moves for current board
        
        Args:
            board_id (PyramidId): The current board state to analyze

        Returns:
            t.Any: return the updated board_moves database
        """
        if _recursion > 14:
            raise RecursionError('Too many levels!')
        ## moves is equal to self._board_moves[peg_count][board_id]
        # with format t.Dict[PegNodeLink: final_board_id]
        moves = self.get_current_board_moves(board_id)
        for new_board in moves.values():
            ## Use _recursion to find moves at the next level
            self.get_all_indiv_board_moves(new_board, _recursion + 1)

    def get_current_board_moves(self, board_id: PyramidId) -> t.List[PegNodeLink]:
        """Determines all the valid moves given the current board state

        Args:
            board_id (PyramidId): The board state to be analyzed

        Returns:
            t.Dict[PegNodeLink, PyramidId]: The valid peg jump moves for this board
        """
        ## self._board_id: dict =
        # { pegs remaining:
        #    { board_id (of current_board):
        #       { move from this board_id: new_board_id after move }}}
        peg_count = board_id.count
        if peg_count in self._board_moves_db:
            current_pegs_dict = self._board_moves_db[peg_count]
        else:
            current_pegs_dict = {}
        if board_id in current_pegs_dict:
            ## if the board_id exists, this was already calculated, just return the old data
            return current_pegs_dict[board_id]
        else:
            current_pegs_dict[board_id] = {}
            moves = self.find_valid_moves(board_id)
            for move in moves:
                new_board = self.get_board_from_move(board_id, move)
                current_pegs_dict[board_id].update({move: new_board})
            ## We just figured out new  moves, store results
            self._board_moves_db[peg_count] = current_pegs_dict
            return current_pegs_dict[board_id]

    def get_board_from_move(self, board_id: PyramidId, move: PegNodeLink) -> PyramidId:
        """Return the board ID that results from taking the given move

        Args:
            board_id (PyramidId): Starting board
            move (PegNodeLink): Peg jump move to take on the starting board

        Raises:
            ValueError: Move is not valid for the starting board

        Returns:
            PyramidId: Resulting board after the move is taken
        """
        if self.move_is_valid(board_id, move):
            pegs = [peg for peg in board_id]
            pegs[move.start] = False
            pegs[move.adjacent] = False
            pegs[move.end] = True
            return PyramidId(*pegs)
        else:
            raise ValueError(f'move {move} is not valid in board, {board_id}')

    def find_valid_moves(self, board_id: PyramidId) -> t.Set[PegNodeLink]:
        """Returns a set of valid jump moves on the given board

        Args:
            board_id (PyramidId): The starting board

        Returns:
            t.Set[PegNodeLink]: A set of all valid moves on the board
        """
        moves = set()
        for node, peg in enumerate(board_id):
            for move in self.test.LINKS[node]:
                if self.move_is_valid(board_id, move):
                    moves.add(move)
        return moves

    def move_is_valid(self, board_id: PyramidId, move: PegNodeLink) -> bool:
        """Determine if move is valid on the given board

        Args:
            board_id (PyramidId): Board to evaluate
            move (PegNodeLink): move to evaluate

        Returns:
            bool: true if move is valid on given board
        """
        return all([
            board_id[move.start],
            board_id[move.adjacent],
            not board_id[move.end],
        ])

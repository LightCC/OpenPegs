import pytest
from src.pegs.PegPyramidAnalyzer import PegPyramidAnalyzer
from src.pegs.PegPyramid import PegPyramid, PyramidId
from src.pegs.PegNodeLink import PegNodeLink


@pytest.fixture()
def sut():
    yield PegPyramidAnalyzer()


@pytest.fixture()
def boards():
    boards = {
        'empty': PyramidId.make(*([False] * 15)),
        'full': PyramidId.make(*([True] * 15)),
        '0-1-2': PyramidId.make(' x xx ooo oooo ooooo '),
        '2-3': PyramidId.make('o ox xoo ooooooooo'),
        '1-5': PyramidId.make('oxoooxooooooooo'),
    }
    yield boards


class TestPegBoardAnalyzer:

    def test_analyzer_base_setup(self, sut, boards):
        PegPyramidAnalyzer._board_moves_db == None
        # sut = PegPyramidAnalyzer()
        sut._board_moves_db == {}
        sut.test.board_id == boards['empty']

    def test_move_is_valid(self, sut, boards):
        # sut = PegPyramidAnalyzer()
        assert sut.move_is_valid(boards['0-1-2'], PegNodeLink(0, 1, 3))
        assert sut.move_is_valid(boards['0-1-2'], PegNodeLink(0, 2, 5))
        assert not sut.move_is_valid(boards['0-1-2'], PegNodeLink(5, 4, 3))
        assert not sut.move_is_valid(boards['0-1-2'], PegNodeLink(1, 3, 6))
        assert not sut.move_is_valid(boards['0-1-2'], PegNodeLink(6, 3, 1))

    def test_find_valid_moves(self, sut, boards):
        moves = sut.find_valid_moves(boards['0-1-2'])
        assert moves == {PegNodeLink(0, 1, 3), PegNodeLink(0, 2, 5)}

    def test_get_board_from_move(self, sut, boards):
        board_id = sut.get_board_from_move(boards['0-1-2'], PegNodeLink(0, 1, 3))
        assert board_id == boards['2-3']
        with pytest.raises(ValueError):
            board_id = sut.get_board_from_move(boards['2-3'], PegNodeLink(7, 8, 9))

    def test_get_current_board_moves(self, sut, boards):
        moves = sut.get_current_board_moves(boards['0-1-2'])
        assert moves == {
            PegNodeLink(0, 1, 3): boards['2-3'],
            PegNodeLink(0, 2, 5): boards['1-5'],
        }

    def test_get_all_indiv_board_moves(self, sut, boards):
        sut.get_all_indiv_board_moves(boards['0-1-2'])
        move_db = sut._board_moves_db
        peg_count_list = [peg_count for peg_count in move_db.keys()]
        moves_3 = move_db[3]
        moves_2 = move_db[2]
        assert sut.move_count_in_board_db == 2
        assert set(peg_count_list) == set((3, 2))
        assert len(moves_3) == 1
        assert moves_3[boards['0-1-2']] == {
            PegNodeLink(0, 2, 5): boards['1-5'],
            PegNodeLink(0, 1, 3): boards['2-3'],
        }
        assert len(moves_2) == 2
        assert moves_2[boards['1-5']] == {}
        assert moves_2[boards['2-3']] == {}

        board = PegPyramid(initial_node=0)
        sut.get_all_indiv_board_moves(board.board_id)
        assert sut.move_count_in_board_db == 10308

    def test_get_all_indiv_board_moves_recursion_error(self, sut, boards):
        board = PegPyramid(initial_node=0)
        with pytest.raises(RecursionError):
            ## Start with just enough recursion to trigger a Recursion error
            sut.get_all_indiv_board_moves(board.board_id, _recursion=2)

    def test_get_all_move_chains(self, sut, boards):
        board = PegPyramid(initial_node=12)
        chains = sut.get_all_move_chains(board.board_id)
        db = sut.board_moves_db
        mdb = sut.move_chains_db

        end_board = PyramidId.make('o oo oxo oooo ooooo')  # board with peg in middle as end board
        found_chains = sut.find_move_chains(end_board_id=end_board)
        assert len(found_chains) == 1550

        # moves = {index: move for index, move in enumerate(mdb) if move[-1][-1] == end_board}
        # print(f'len(moves) = {len(moves)}')

        print('test')

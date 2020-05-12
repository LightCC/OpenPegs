import pytest
from src.pegs.PegPyramidAnalyzer import PegPyramidAnalyzer
from src.pegs.PegPyramid import PegPyramid
from src.pegs.PegNodeLink import PegNodeLink


@pytest.fixture()
def sut():
    yield PegPyramidAnalyzer()


@pytest.fixture()
def boards():
    boards = {
        'empty': PegPyramid.State(*([False] * 15)),
        'full': PegPyramid.State(*([True] * 15)),
        '0-1-2': PegPyramid.State(True, True, True),
        '2-3': PegPyramid.State(False, False, True, True),
    }
    yield boards


class TestPegBoardAnalyzer:

    def test_analyzer_base_setup(self, sut, boards):
        PegPyramidAnalyzer._board_moves == None
        # sut = PegPyramidAnalyzer()
        sut._board_moves == {}
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
        raise NotImplementedError

    def test_analyze_game_board(self, sut, boards):
        raise NotImplementedError

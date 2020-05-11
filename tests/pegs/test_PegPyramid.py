import pytest
from src.pegs.PegPyramid import PegPyramid
from src.pegs.PegNodeLink import PegNodeLink


class TestPegPyramid:

    def test_PegPyramid_basic_init(self):
        pyramid = PegPyramid()
        assert pyramid.nodes_string() == (  #
            '    0    \n'
            '   1 2   \n'
            '  3 4 5  \n'
            ' 6 7 8 9 \n'
            'a b c d e'
        )
        assert pyramid.pegs_string() == (  #
            '    o    \n'
            '   o o   \n'
            '  o o o  \n'
            ' o o o o \n'
            'o o o o o'
        )
        pyramid.add_peg(3)
        pyramid.add_peg(4)
        assert pyramid.pegs_string() == (  #
            '    o    \n'
            '   o o   \n'
            '  x x o  \n'
            ' o o o o \n'
            'o o o o o'
        )
        pyramid.pegs = True
        assert pyramid.pegs_string() == (  # 
            '    x    \n'
            '   x x   \n'
            '  x x x  \n'
            ' x x x x \n'
            'x x x x x'
        )
        assert pyramid.full_string(
        ) == (  #
            '            0:x            \n'
            '         1:x   2:x         \n'
            '      3:x   4:x   5:x      \n'
            '   6:x   7:x   8:x   9:x   \n'
            'a:x   b:x   c:x   d:x   e:x'
        )
        assert pyramid.node_and_pegs_string() == (  #
            '    0           x    \n'
            '   1 2         x x   \n'
            '  3 4 5       x x x  \n'
            ' 6 7 8 9     x x x x \n'
            'a b c d e   x x x x x'
        )

    def test_analyze_current_game_board_runs(self):
        pyramid = PegPyramid()
        result = pyramid.analyze_current_game_board()
        assert result == []
        pyramid.add_peg(10)
        pyramid.add_peg(11)
        result = pyramid.analyze_current_game_board()
        assert result == pyramid.valid_moves

    def test_analyze_final_move(self):
        """
        Test analysis of a board with a single possible final move
        """
        # Setup with pegs in nodes 1 and 2
        pyramid = PegPyramid()
        pyramid.pegs = False
        pyramid.add_peg(0)
        pyramid.add_peg(1)
        # Only move left is jump 0->1->3
        results = pyramid.analyze_current_game_board()
        assert len(results) == 1
        assert str(results[0]) == '0->1->3'

    def test_board_id(self):
        pyramid = PegPyramid()
        empty_board = PegPyramid.State(*([False] * 15))
        assert pyramid.board_id == empty_board
        pyramid.pegs = True
        full_board = PegPyramid.State(*([True] * 15))
        assert pyramid.board_id == full_board

    def test_board_id_restore(self):
        pyramid = PegPyramid()
        empty_board = PegPyramid.State(*([False] * 15))
        full_board = PegPyramid.State(*([True] * 15))
        assert pyramid.count_pegs() == 0
        pyramid.board_id = full_board
        assert pyramid.count_pegs() == 15
        pyramid.board_id = empty_board
        assert pyramid.count_pegs() == 0
        board_123 = PegPyramid.State(*([True] * 3 + [False] * 12))
        pyramid.board_id = board_123
        assert pyramid.count_pegs() == 3
        assert pyramid.pegs_string() == (  #
            '    x    \n'
            '   x x   \n'
            '  o o o  \n'
            ' o o o o \n'
            'o o o o o'
        )

    def test_executing_a_jump_move(self):
        pyramid = PegPyramid()
        pyramid.setup_game_board_from_initial_node(1)
        link_4_2_1 = PegNodeLink(4, 2, 1)
        # Jump from 4 to 1, removing 2
        pyramid.execute_jump_move(link_4_2_1)
        # Try to jump from 4, but no peg there
        link_4_5_6 = PegNodeLink(4, 5, 6)
        with pytest.raises(ValueError):
            pyramid.execute_jump_move(link_4_5_6)
        # Try to jump 7->4->2, but no peg in 4 to jump!
        link_7_4_2 = PegNodeLink(7, 4, 2)
        with pytest.raises(ValueError):
            pyramid.execute_jump_move(link_7_4_2)
        # Try to jump 7->8->9, but a peg is already in 9!
        link_7_8_9 = PegNodeLink(7, 8, 9)
        with pytest.raises(ValueError):
            pyramid.execute_jump_move(link_7_8_9)

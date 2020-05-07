import pytest
from src.pegs.PegPyramid import PegPyramid
from src.pegs.PegNodeLink import PegNodeLink


class TestPegPyramid:

    def test_PegPyramid_basic_init(self):
        pyramid = PegPyramid()
        assert pyramid.nodes_str() == (  #
            '    1    \n'
            '   2 3   \n'
            '  4 5 6  \n'
            ' 7 8 9 a \n'
            'b c d e f'
        )
        assert pyramid.pegs_str() == (  #
            '    o    \n'
            '   o o   \n'
            '  o o o  \n'
            ' o o o o \n'
            'o o o o o'
        )
        pyramid.node(4).add_peg()
        pyramid.node(5).add_peg()
        assert pyramid.pegs_str() == (  #
            '    o    \n'
            '   o o   \n'
            '  x x o  \n'
            ' o o o o \n'
            'o o o o o'
        )
        pyramid.pegs = True
        assert pyramid.pegs_str() == (  # 
            '    x    \n'
            '   x x   \n'
            '  x x x  \n'
            ' x x x x \n'
            'x x x x x'
        )
        assert pyramid.full_str(
        ) == (  #
            '            1:x            \n'
            '         2:x   3:x         \n'
            '      4:x   5:x   6:x      \n'
            '   7:x   8:x   9:x   a:x   \n'
            'b:x   c:x   d:x   e:x   f:x'
        )
        assert pyramid.node_and_pegs_str() == (  #
            '    1           x    \n'
            '   2 3         x x   \n'
            '  4 5 6       x x x  \n'
            ' 7 8 9 a     x x x x \n'
            'b c d e f   x x x x x'
        )

    def test_analyze_current_game_board_runs(self):
        pyramid = PegPyramid()
        pyramid.analyze_current_game_board()

    def test_analyze_final_move(self):
        """
        Test analysis of a board with a single possible final move
        """
        # Setup with pegs in nodes 1 and 2
        pyramid = PegPyramid()
        pyramid.pegs = False
        pyramid.node(1).peg_is_present = True
        pyramid.node(2).peg_is_present = True
        # Only move left is jump 1->2->4
        results = pyramid.analyze_current_game_board()
        assert len(results) == 1
        assert str(results[0]) == '1->2->4'

    def test_board_id(self):
        pyramid = PegPyramid()
        assert pyramid.board_id() == 0
        pyramid.pegs = True
        MAX_BOARD_ID = (1 << len(pyramid.node_ids)) - 1
        assert pyramid.board_id() == MAX_BOARD_ID

    def test_executing_a_jump_move(self):
        pyramid = PegPyramid()
        pyramid.setup_game_board(1)
        link_4_2_1 = PegNodeLink(pyramid.node(4), pyramid.node(2), pyramid.node(1))
        # Jump from 4 to 1, removing 2
        pyramid.execute_jump_move(link_4_2_1)
        # Try to jump from 4, but no peg there
        link_4_5_6 = PegNodeLink(pyramid.node(4), pyramid.node(5), pyramid.node(6))
        with pytest.raises(ValueError):
            pyramid.execute_jump_move(link_4_5_6)
        # Try to jump 7->4->2, but no peg in 4 to jump!
        link_7_4_2 = PegNodeLink(pyramid.node(7), pyramid.node(4), pyramid.node(2))
        with pytest.raises(ValueError):
            pyramid.execute_jump_move(link_7_4_2)
        # Try to jump 7->8->9, but a peg is already in 9!
        link_7_8_9 = PegNodeLink(pyramid.node(7), pyramid.node(8), pyramid.node(9))
        with pytest.raises(ValueError):
            pyramid.execute_jump_move(link_7_8_9)

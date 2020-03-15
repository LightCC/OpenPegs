import pytest
from src.pegs.PegPyramid import PegPyramid

class TestPegPyramid:
    def test_PegPyramid_basic_init(self):
        pyramid = PegPyramid()
        assert pyramid.nodes_str() == ('    1    \n'
                                       '   2 3   \n'
                                       '  4 5 6  \n'
                                       ' 7 8 9 a \n'
                                       'b c d e f')
        assert pyramid.pegs_str() == ('    o    \n'
                                      '   o o   \n'
                                      '  o o o  \n'
                                      ' o o o o \n'
                                      'o o o o o')
        pyramid.node(4).add_peg()
        pyramid.node(5).add_peg()
        assert pyramid.pegs_str() == ('    o    \n'
                                      '   o o   \n'
                                      '  x x o  \n'
                                      ' o o o o \n'
                                      'o o o o o')
        pyramid.set_pegs(True)
        assert pyramid.pegs_str() == ('    x    \n'
                                      '   x x   \n'
                                      '  x x x  \n'
                                      ' x x x x \n'
                                      'x x x x x')
        assert pyramid.full_str() == ('            1:x            \n'
                                      '         2:x   3:x         \n'
                                      '      4:x   5:x   6:x      \n'
                                      '   7:x   8:x   9:x   a:x   \n'
                                      'b:x   c:x   d:x   e:x   f:x')
        assert pyramid.node_and_pegs_str() == ('    1           x    \n'
                                               '   2 3         x x   \n'
                                               '  4 5 6       x x x  \n'
                                               ' 7 8 9 a     x x x x \n'
                                               'b c d e f   x x x x x')

    def test_analyze_current_game_board_runs(self):
        pyramid = PegPyramid()
        pyramid.analyze_current_game_board()
        
    def test_analyze_final_move(self):
        """
        Test analysis of a board with a single possible final move
        """
        # Setup with pegs in nodes 1 and 2
        pyramid = PegPyramid()
        pyramid.set_pegs(False)
        pyramid.node(1).set_peg(True)
        pyramid.node(2).set_peg(True)
        # Only move left is jump 1->2->4
        results = pyramid.analyze_current_game_board()
        assert len(results) == 1
        assert str(results[0]) == '1->2->4'
        
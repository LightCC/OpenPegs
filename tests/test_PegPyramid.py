import pytest
from src.PegPyramid import PegPyramid

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
        for node_id in pyramid.nodes():
            pyramid.node(node_id).set_peg()
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


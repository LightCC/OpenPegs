import pytest
from src.pegs.PegBoard import PegBoard
from src.pegs.PegException import *


@pytest.fixture()
def board6():
    nodelist = {node: str(node) for node in range(1, 7)}
    # links = [(1, 2, 3), (1, 6, 5), (3, 2, 1), (3, 4, 5), (5, 4, 3), (5, 6, 1)]
    format_str = (  #
        "  {x[0]}  \n"
        " {x[1]} {x[2]} \n"
        "{x[3]} {x[4]} {x[5]}"
    )
    yield PegBoard(nodelist, format_str)


@pytest.fixture()
def board3():
    nodelist = {node: str(node) for node in range(1, 4)}
    # links = [(1, 2, 3), (3, 1, 2), (2, 3, 1)]
    format_str = (  #
        " {x[0]} \n"
        "{x[1]} {x[2]}"
    )
    yield PegBoard(nodelist, format_str)


class TestPegBoard_Main:

    def test_basic_PegBoard_object_creation(self, board6):
        '''Ensure that basic PegBoard object creation is working correctly.
        '''
        nodes = [x for x in range(1, 7)]
        nodelist = {node: str(node) for node in nodes}
        assert board6._nodes_str == nodelist
        assert board6.nodes == nodes

    def test_format_string_outputs(self, board3):
        '''test the creation of a format_str
        
        Whether a format string is working is tested by the outputs of .node_str(), .pegs_string(), .full_string(), and .node_and_pegs_string().
        '''

        # Setup a format string in a pyramid, for just nodes 1-3
        test_str = (' {x[0]} \n' '{x[1]} {x[2]}')
        board3.format_str = test_str
        assert board3.format_str == test_str
        assert board3.nodes_string() == (  #
            ' 1 \n'
            '2 3'
        )
        assert board3.nodes_string(indent=2) == (  #
            '   1 \n'
            '  2 3'
        )
        assert board3.pegs_string() == (  #
            ' o \n'
            'o o'
        )

        ## Set a pegs different ways in first 3 nodes
        board3.pegs = True
        assert board3.pegs_string() == (' x \n' 'x x')
        assert board3.pegs_string(1) == ('  x \n' ' x x')
        assert board3.full_string() == ('   1:x   \n' '2:x   3:x')
        assert board3.full_string(indent=5) == ('        1:x   \n' '     2:x   3:x')
        assert board3.node_and_pegs_string() == (' 1     x \n' '2 3   x x')
        assert board3.node_and_pegs_string(indent=3, space_between=0) == ('    1  x \n' '   2 3x x')

    def test_set_pegs_with_single_value(self, board6):
        board6.pegs = True
        assert all([board6.peg(node) == True for node in board6.nodes])
        board6.pegs = False
        assert all([board6.peg(node) == False for node in board6.nodes])
        board6.pegs = 1
        assert all([board6.peg(node) == True for node in board6.nodes])
        board6.pegs = 0
        assert all([board6.peg(node) == False for node in board6.nodes])

    def test_set_pegs_with_dict(self, board6):
        pegs = {node_id: True for node_id in board6.nodes}
        assert all([board6.peg(node) == False for node in board6.nodes])
        board6.pegs = pegs
        assert all([board6.peg(node) == True for node in board6.nodes])
        pegs[1] = False
        pegs[4] = False
        pegs[6] = False
        board6.pegs = pegs
        pegs_list = [board6.peg(node) for node in board6.nodes]
        pegs_test = [False, True, True, False, True, False]
        assert pegs_list == pegs_test
        ## Test setting with a list
        # Reset to all True (use 1 for fun)
        board6.pegs = 1
        for node in board6.nodes:
            assert board6.peg(node)

    def test_raise_exception_on_failed_add_or_remove_peg(self, board6):
        assert board6.count_pegs() == 0
        with pytest.raises(PegNotAvailable):
            board6.remove_peg(1)
        board6.add_peg(1)
        with pytest.raises(PegAlreadyPresent):
            board6.add_peg(1)
        board6.count_pegs() == 1
        board6.remove_peg(1)
        board6.count_pegs() == 0

    def test_set_add_remove_pegs_with_node_str(self, board6):
        assert board6.count_pegs() == 0
        assert board6.peg(1) == False
        board6._set_peg('1', True)
        assert board6.peg('1') == True
        board6.remove_peg('1')
        assert board6.peg('1') == False
        assert board6.peg_str('1') == 'o'
        board6.add_peg('1')
        assert board6.peg('1') == True
        assert board6.peg_str('1') == 'x'

    def test_count_pegs(self, board6):
        """test the .count_pegs() function
        
        .count_pegs() should return the number of pegs currently on the board
        """
        assert board6.count_pegs() == 0
        board6.pegs = True
        assert board6.count_pegs() == 6
        board6.remove_peg(1)
        board6.remove_peg(4)
        board6.remove_peg(5)
        assert board6.count_pegs() == 3

    def test_node_ids_str_is_correct(self, board3):
        assert board3._nodes_str == {1: '1', 2: '2', 3: '3'}

    def test_set_add_remove_pegs(self, board6):
        pegs_0 = {x: False for x in range(1, 7)}
        pegs_6 = {x: True for x in range(1, 7)}
        pegs126 = {1: True, 2: True, 3: False, 4: False, 5: False, 6: True}
        assert board6.pegs == pegs_0
        board6.pegs = pegs_6
        assert board6.pegs == pegs_6
        board6.pegs = False
        assert board6.pegs == pegs_0
        board6.pegs = True
        assert board6.pegs == pegs_6
        board6.pegs = pegs126
        assert board6.pegs == pegs126
        assert [board6.peg(node) for node in range(1, 7)] == [peg for peg in pegs126.values()]
        board6.remove_peg(1)
        board6.remove_peg(2)
        board6.remove_peg(6)
        assert board6.pegs == pegs_0
        board6.add_peg(1)
        board6.add_peg(2)
        board6.add_peg(6)
        assert board6.pegs == pegs126
        assert board6.count_pegs() == 3
        board6._set_peg(1, False)
        assert board6.count_pegs() == 2
        board6._set_peg(2, False)
        assert board6.count_pegs() == 1
        board6._set_peg(6, False)
        assert board6.pegs == pegs_0
        board6._set_peg(1, True)
        assert board6.count_pegs() == 1
        board6._set_peg(2, True)
        assert board6.count_pegs() == 2
        board6._set_peg(6, True)
        assert board6.count_pegs() == 3
        assert board6.pegs == pegs126
        assert board6.peg_str(1) == 'x'
        assert board6.peg_str(3) == 'o'
        board6._set_peg(3, True)
        assert board6.peg_str(3) == 'x'


class TestPegBoard_FormatStr:

    def test_format_str_basic(self):
        nodes = {1: '1', 2: 'b', 3: '%'}
        rows = [[1], [2, 3]]
        format_str = PegBoard._create_format_str(nodes, rows)
        assert format_str == ' {x[0]} \n{x[1]} {x[2]}'
        board = PegBoard(nodes, format_str)
        assert board.nodes_string() == ' 1 \nb %'
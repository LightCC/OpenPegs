import pytest
from src.pegs.PegBoard import PegBoard
from src.pegs.PegNode import PegNode
from src.pegs.PegNodeLink import PegNodeLink


def fake_function():
    pass


@pytest.fixture(params=[1, 1.1, {1, 2, 3}, 'string', {1: 1, 2: '2'}, (1, '1'), fake_function])
def not_a_list(request):
    '''A test fixture "not_a_list" that can be used as an argument to supply parameterized test cases that have separate objects of different types that are not of type <list>
    '''
    return request.param


@pytest.fixture(params=[1, 1.1, {'1', '2', '3'}, ['1', '2', '3'], {'1': '1', '2': '2'}, ('1', '1'), fake_function])
def not_a_string(request):
    '''A test fixture "not_a_string" that provides multiple parameterized test cases with separate objects that are not of type <str>
    '''
    return request.param


class TestPegBoard:

    def test_basic_PegBoard_object_creation(self):
        '''Ensure that basic PegBoard object creation is working correctly. i.e. Node objects are created that return the correct node ids, and different methods of accessing them through the .nodes and .node(node_id) functions work.
        '''
        nodelist = [PegNode(1), PegNode(2)]
        board = PegBoard(nodelist)
        assert len(board.nodes) == 2
        assert board.node(1).node_id == 1
        assert board.node(2).node_id == 2
        assert board.node(1) == nodelist[0]
        assert board.node(2) == nodelist[1]
        for node in nodelist:
            assert node in board.nodes

    def test_format_string_outputs(self):
        '''test the creation of a format_str
        
        Whether a format string is working is tested by the outputs of .node_str(), .pegs_str(), .full_str(), and .node_and_pegs_str().
        '''
        node_ids = [1, 2, 3]
        nodelist = [PegNode(node_id) for node_id in node_ids]
        board = PegBoard(nodelist)
        # Setup a format string in a pyramid
        test_str = (' {x[0]} \n' '{x[1]} {x[2]}')
        board.format_str = test_str
        assert board.format_str == test_str
        assert board.nodes_str() == (' 1 \n' '2 3')
        assert board.nodes_str(indent=2) == ('   1 \n' '  2 3')
        assert board.pegs_str() == (' o \n' 'o o')

        ## Set a peg in every position (switch from o's to x's)
        for node in board.nodes:
            node.add_peg()
        assert board.pegs_str() == (' x \n' 'x x')
        assert board.pegs_str(1) == ('  x \n' ' x x')
        assert board.full_str() == ('   1:x   \n' '2:x   3:x')
        assert board.full_str(indent=5) == ('        1:x   \n' '     2:x   3:x')
        assert board.node_and_pegs_str() == (' 1     x \n' '2 3   x x')
        assert board.node_and_pegs_str(indent=3, space_between=0) == ('    1  x \n' '   2 3x x')

    def test_raises_ValueError_if_format_string_is_not_set(self):
        '''Ensure a ValueError is raised if the .format_str function is called before the .format_str property is set by the parent
        '''
        nodelist = [PegNode(1), PegNode(2)]
        board = PegBoard(nodelist)
        with pytest.raises(ValueError):
            board.format_str

    def test_raises_ValueError_if_nodelist_is_invalid(self, not_a_list):
        '''Ensure a ValueError is raised when creating a PegBoard with either a node_ids or node_ids_str argument that are not a list
        '''
        ## Test that nodelist which is not a list raises ValueError
        with pytest.raises(ValueError):
            PegBoard(not_a_list)
        # convert the invalid nodelist into a list that has invalid items (i.e. they are not PegNode type), either by adding each item in the object to a list, or adding the object directly as the only item in a list
        try:
            nodelist_with_invalid_items = [x for x in not_a_list]
        except TypeError:  # TypeError is thrown if node_ids is not iterable
            nodelist_with_invalid_items = [not_a_list]
        # Use the nodelist with a invalid items that are not PegNodes, and ensure a ValueError is raised
        with pytest.raises(ValueError):
            PegBoard(nodelist_with_invalid_items)

    def test_set_pegs_with_single_value(self):
        nodelist = [PegNode(node_id) for node_id in range(1, 16)]
        pyramid = PegBoard(nodelist)
        pyramid.pegs = True
        assert all([node.peg_is_present == True for node in pyramid.nodes])
        pyramid.pegs = False
        assert all([node.peg_is_present == False for node in pyramid.nodes])
        pyramid.pegs = 1
        assert all([node.peg_is_present == True for node in pyramid.nodes])
        pyramid.pegs = 0
        assert all([node.peg_is_present == False for node in pyramid.nodes])

    def test_set_pegs_with_dict(self):
        nodelist = [PegNode(node_id) for node_id in range(1, 16)]
        pyramid = PegBoard(nodelist)
        pegs = {node_id: True for node_id in pyramid.node_ids}
        pyramid.pegs = pegs
        assert all([node.peg_is_present == True for node in pyramid.nodes])
        pegs[1] = False
        pegs[4] = False
        pegs[6] = False
        pegs[15] = False
        pyramid.pegs = pegs
        pegs_list = [node.peg_is_present for node in pyramid.nodes]
        pegs_test = [False, True, True, False, True, False, True, True, True, True, True, True, True, True, False]
        assert pegs_list == pegs_test
        ## Test setting with a list
        # Reset to all True (use 1 for fun)
        pyramid.pegs = 1
        assert all([node.peg_is_present == True for node in pyramid.nodes])

    def test_count_pegs(self):
        """test the .count_nodes_with_pegs() function
        
        .count_nodes_with_pegs() should return the number of pegs currently on the board
        """
        nodelist = [PegNode(x) for x in [1, 2, 3, 4, 5]]
        board = PegBoard(nodelist)
        assert board.count_nodes_with_pegs() == 0
        board.pegs = True
        assert board.count_nodes_with_pegs() == 5
        board.node(1).remove_peg()
        board.node(4).remove_peg()
        board.node(5).remove_peg()
        assert board.count_nodes_with_pegs() == 2

    def test_node_ids_str_is_correct(self):
        nodelist = [PegNode(1), PegNode(2), PegNode(3)]
        board = PegBoard(nodelist)
        assert board.node_ids_str == {1: '1', 2: '2', 3: '3'}

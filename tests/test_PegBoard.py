import pytest
from src.PegBoard import PegBoard
from src.PegNode import PegNode
from src.PegNodeLink import PegNodeLink

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
        '''Ensure that basic PegBoard object creation is working correctly. i.e. Node objects are created that return the correct node ids, and different methods of accessing them through the .nodes() and .node(node_id) functions work.
        '''
        node_ids = [1, 2]
        board = PegBoard(node_ids)
        nodes = board.nodes()
        assert len(nodes) == 2
        assert board.node(1).node_id() == 1
        assert board.node(2).node_id() == 2
        assert nodes[1] is board.node(1)
        assert nodes[2] is board.node(2)
    
    def test_format_string_outputs(self):
        '''test the creation of a format_str
        
        Whether a format string is working is tested by the outputs of .node_str(), .pegs_str(), .full_str(), and .node_and_pegs_str().
        '''
        node_ids = [1, 2, 3]
        board = PegBoard(node_ids)
        # Setup a format string in a pyramid
        test_str = (' {x[0]} \n'
                    '{x[1]} {x[2]}')
        board._format_str = test_str
        assert board.format_str() == test_str
        assert board.nodes_str() == (' 1 \n'
                                     '2 3')
        assert board.nodes_str(indent=2) == ('   1 \n'
                                             '  2 3')
        assert board.pegs_str() == (' o \n'
                                    'o o')
        
        ## Set a peg in every position (switch from o's to x's)
        for node in board.nodes().values():
            node.set_peg()
        assert board.pegs_str() == (' x \n'
                                    'x x')
        assert board.pegs_str(1) == ('  x \n'
                                     ' x x')
        assert board.full_str() == ('   1:x   \n'
                                    '2:x   3:x')
        assert board.full_str(indent=5) == ('        1:x   \n'
                                            '     2:x   3:x')
        assert board.node_and_pegs_str() == (' 1     x \n'
                                             '2 3   x x')
        assert board.node_and_pegs_str(indent=3, space_between=0) == ('    1  x \n'
                                             '   2 3x x')
    def test_raises_ValueError_if_format_string_is_not_set(self):
        '''Ensure a ValueError is raised if the .format_str() function is called before the ._format_str property is set by the parent
        '''
        node_ids = [1, 2]
        board = PegBoard(node_ids)
        with pytest.raises(ValueError):
            board.format_str()
    
    def test_raises_ValueError_if_node_ids_or_node_ids_str_are_not_a_list(self, not_a_list):
        '''Ensure a ValueError is raised when creating a PegBoard with either a node_ids or node_ids_str argument that are not a list
        '''
        ## Test an node_ids that is not a list raises ValueError)
        with pytest.raises(ValueError):
            PegBoard(not_a_list)
        # convert the invalid node_ids into a list that is valid, either by adding each item in the object to a list, or adding the object directly as the only item in a list
        try:
            valid_node_ids = [ x for x in not_a_list ]
        except TypeError: # TypeError is thrown if node_ids is not iterable
            valid_node_ids = [ not_a_list ]
        # Use the valid node_ids value with a node_ids_str that is not a list, and ensure a ValueError is raised        
        with pytest.raises(ValueError):
            PegBoard(valid_node_ids, node_ids_str=not_a_list)
        # Now test with both invalid
        with pytest.raises(ValueError):
            PegBoard(not_a_list, not_a_list)
        
    def test_raises_ValueError_if_arg_lengths_are_not_equal(self):
        '''Ensure a ValueError is raised if the node_ids and node_ids_str are both provided, and are both lists, but are not the same length
        '''
        node_ids = [1, 2, 3]
        node_ids_str = ['1', '2']
        with pytest.raises(ValueError):
            PegBoard(node_ids, node_ids_str=node_ids_str)
        
    def test_raises_ValueError_if_node_ids_str_arg_items_are_not_strings(self, not_a_string):
        '''Ensure a ValueError is raised if any item in the node_ids_str argument are not a string, when node_ids_str is provided and is a list (i.e. is not the empty string, which is default and will auto-create a list of strings from the node_ids).
        '''
        node_ids = [1, 2, 3]
        node_ids_str = ['1', '2', '3']
        # No Exception should be raised
        PegBoard(node_ids, node_ids_str=node_ids_str)
        
        # Set up three test lists with the current non-string in each of the 3 positions in the list then ensure it generates a ValueError
        node_ids_str_test1 = [not_a_string, '2', '3']
        with pytest.raises(ValueError):
            PegBoard(node_ids, node_ids_str=node_ids_str_test1)
        
        node_ids_str_test2 = ['1', not_a_string, '3']
        with pytest.raises(ValueError):
            PegBoard(node_ids, node_ids_str=node_ids_str_test2)
        
        node_ids_str_test3 = ['1', '2', not_a_string]
        with pytest.raises(ValueError):
            PegBoard(node_ids, node_ids_str=node_ids_str_test3)

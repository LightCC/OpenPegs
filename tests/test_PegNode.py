import pytest
from src.PegNode import PegNode

def fake_function():
    pass

## supplies valid (node_id, node_id_str)
@pytest.fixture(params=[(1, '1'), ('string', 'string'), (1.1, '1.1')])
def valid_node_id_type(request):
    return request.param

## supplies values that are not strings
@pytest.fixture(params=[1, 1.1, ['1.1'], {2, 1}, fake_function, ('abc', 'def')])
def not_a_string(request):
    return request.param

class TestPegNode:
    def test_init_sets_node_id_and_string(self, valid_node_id_type):
        (node_id, node_id_str) = valid_node_id_type
        node = PegNode(None, node_id, node_id_str)
        assert node.node_id() == node_id
        assert node.node_id_str() == node_id_str

    def test_generates_correct_node_id_string(self, valid_node_id_type):
        node_id, node_id_str = valid_node_id_type
        node = PegNode(None, node_id)
        assert node.node_id_str() == node_id_str
            
    def test_init_raises_valueerror_if_node_id_str_arg_is_not_str(self, not_a_string):
        with pytest.raises(ValueError):
            PegNode(None, 1, node_id_str=not_a_string)
            
    def test_init_peg_at_initialization(self):
        node_peg_false = PegNode(None, 1, peg=False)
        assert node_peg_false.peg() == False
        assert node_peg_false.peg_str() == 'o'
        node_peg_false2 = PegNode(None, 1, peg=0)
        assert node_peg_false2.peg() == False
        assert node_peg_false2.peg_str() == 'o'
        node_peg_true = PegNode(None, 2, peg=True)
        assert node_peg_true.peg() == True
        assert node_peg_true.peg_str() == 'x'
        node_peg_true2 = PegNode(None, 2, peg=9999)
        assert node_peg_true2.peg() == True
        assert node_peg_true2.peg_str() == 'x'
        
    def test_setting_and_removing_pegs(self):
        node = PegNode(None, 1)
        assert node.peg() == False
        # With peg not present, should have error clearing it
        with pytest.raises(ValueError):
            node.clear_peg()
        node.set_peg()
        assert node.peg() == True
        # With peg already present, should have error setting it
        with pytest.raises(ValueError):
            node.set_peg()
        node.clear_peg()
        assert node.peg() == False
        
        
    def test_add_links_to_node(self):
        nodes = {}
        ## Make 4 nodes that can be linked
        # will be in diamond pattern
        # 1 -> 2 -> 4
        # 1 -> 3 -> 4
        # and reverse from 4 to 1 on each path
        node1 = PegNode(nodes, 1)
        node2 = PegNode(nodes, 2)
        node3 = PegNode(nodes, 3)
        node4 = PegNode(nodes, 4)
        nodes.update({1: node1, 2: node2, 3: node3, 4: node4})
        node1.add_link(node2, node4)
        assert len(node1._links) == 1
        node1.add_link(node3, node4)
        assert len(node1._links) == 2
        node4.add_link(node2, node1)
        assert len(node4._links) == 1
        node4.add_link(node3, node1)
        assert len(node1._links) == 2
        assert len(node2._links) == 0
        assert len(node3._links) == 0
        assert len(node4._links) == 2
        assert node1._links[0]._start_node is node1
        assert node1._links[0]._adjacent_node is node2
        assert node1._links[0]._end_node is node4
        assert node1._links[1]._start_node is node1
        assert node1._links[1]._adjacent_node is node3
        assert node1._links[1]._end_node is node4
        assert node4._links[1]._start_node is node4
        assert node4._links[1]._adjacent_node is node3
        assert node4._links[1]._end_node is node1
        assert str(node1._links[0]) == '1->2->4'
        assert str(node1._links[1]) == '1->3->4'
        assert str(node4._links[0]) == '4->2->1'        
        assert str(node4._links[1]) == '4->3->1'
        assert node1._links[0]._end_node._parent[1] is node1
        assert node1._links[0]._end_node._parent[4] is node4
        assert len(node4._parent) == 4
        assert len(node1._parent) == 4
        
        ## Test the .links() method
        links = node1.links()
        assert links is node1._links
        
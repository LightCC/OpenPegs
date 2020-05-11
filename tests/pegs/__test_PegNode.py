import pytest
from src.pegs.PegNode import PegNode
from src.pegs.PegNodeId import PegNodeId
from src.pegs.PegNodePeg import PegNodePeg
from src.pegs.PegNodeLink import PegNodeLink
from src.pegs.PegException import PegAlreadyPresent, PegNotAvailable


def fake_function():
    pass


## supplies valid (node_id, id_str)
@pytest.fixture(params=[(1, '1'), (-99, '-99'), (9876, '9876')])
def valid_node_id_type(request):
    return request.param


## supplies values that are not strings
@pytest.fixture(params=[1, 1.1, ['1.1'], {2, 1}, fake_function, ('abc', 'def')])
def not_a_string(request):
    return request.param


class TestPegNode:

    def test_init_sets_node_id_and_string(self, valid_node_id_type):
        (node_id, id_str) = valid_node_id_type
        node = PegNode(node_id, id_str=id_str)
        assert node.node_id == node_id
        assert node.node_id_str == id_str

    def test_init_raises_valueerror_if_node_id_str_arg_is_not_str(self, not_a_string):
        with pytest.raises(ValueError):
            PegNode(1, id_str=not_a_string)

    def test_peg_at_initialization(self):
        node_peg_default = PegNode(1)
        assert not node_peg_default.peg_is_present
        assert node_peg_default.peg_str == 'o'
        node_peg_false2 = PegNode(1, peg_is_present=0)
        assert not node_peg_false2.peg_is_present
        assert node_peg_false2.peg_str == 'o'
        node_peg_false2 = PegNode(1, peg_is_present=False)
        assert not node_peg_false2.peg_is_present
        assert node_peg_false2.peg_str == 'o'
        node_peg_true = PegNode(2, peg_is_present=True)
        assert node_peg_true.peg_is_present
        assert node_peg_true.peg_str == 'x'
        node_peg_true2 = PegNode(2, peg_is_present=9999)
        assert node_peg_true2.peg_is_present
        assert node_peg_true2.peg_str == 'x'

    def test_adding_and_removing_pegs(self):
        node = PegNode(1)
        assert node.peg_is_present == False
        # With peg not present, should have error clearing it
        with pytest.raises(PegNotAvailable):
            node.remove_peg()
        node.add_peg()
        assert node.peg_is_present == True
        # With peg already present, should have error setting it
        with pytest.raises(PegAlreadyPresent):
            node.add_peg()
        node.remove_peg()
        assert node.peg_is_present == False

    def test_set_peg_directly(self):
        """set_peg(peg_value) will set whether a peg is present directly, regardless of whether the node currently has a peg or not. This is different from .add_peg and .remove_peg which will fail if there is already a peg present when adding or there is no peg to remove.
        """
        node = PegNode(1)
        assert not node.peg_is_present
        node.peg_is_present = False
        assert not node.peg_is_present
        node.peg_is_present = True
        assert node.peg_is_present
        node.peg_is_present = True
        assert node.peg_is_present
        node.peg_is_present = False
        assert not node.peg_is_present

    def test_add_links_to_node(self):
        nodes = {}
        ## Make 4 nodes that can be linked
        # will be in diamond pattern
        # 1 -> 2 -> 4
        # 1 -> 3 -> 4
        # and reverse from 4 to 1 on each path
        node1 = PegNode(1)
        node2 = PegNode(2)
        node3 = PegNode(3)
        node4 = PegNode(4)
        nodes.update({1: node1, 2: node2, 3: node3, 4: node4})
        for node in nodes.values():
            node.parent = nodes
        node1.add_link(node2, node4)
        assert len(node1.links) == 1
        node1.add_link(node3, node4)
        assert len(node1.links) == 2
        node4.add_link(node2, node1)
        assert len(node4.links) == 1
        node4.add_link(node3, node1)
        assert len(node1.links) == 2
        assert len(node2.links) == 0
        assert len(node3.links) == 0
        assert len(node4.links) == 2
        assert node1.links[0].start_node is node1
        assert node1.links[0].adjacent_node is node2
        assert node1.links[0].end_node is node4
        assert node1.links[1].start_node is node1
        assert node1.links[1].adjacent_node is node3
        assert node1.links[1].end_node is node4
        assert node4.links[1].start_node is node4
        assert node4.links[1].adjacent_node is node3
        assert node4.links[1].end_node is node1
        assert str(node1.links[0]) == '1->2->4'
        assert str(node1.links[1]) == '1->3->4'
        assert str(node4.links[0]) == '4->2->1'
        assert str(node4.links[1]) == '4->3->1'
        assert node1.links[0].end_node.parent[1] is node1
        assert node1.links[0].end_node.parent[4] is node4
        assert len(node4.parent) == 4
        assert len(node1.parent) == 4

        ## Test the .links method
        links = node1.links
        assert links is node1.links

    def test_PegNode_string_output(self):
        node1 = PegNode(1)
        node2 = PegNode(2)
        node3 = PegNode(3)
        node1.add_link(node2, node3)

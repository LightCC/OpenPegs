import pytest
from src.pegs.PegNodeId import PegNodeId


class TestPegNodeId:

    def test_create_PegNodeId(self):
        """Test generic PegNodeId initializations"""
        idx = PegNodeId(99, '99')
        assert idx == 99
        assert str(idx) == '99'

        idx = PegNodeId(-5, 'minus five')
        assert idx == -5
        assert idx._id_str == 'minus five'
        assert str(idx) == 'minus five'

    def test_two_node_ids_are_equal(self):
        id1 = PegNodeId(1, '1')
        id2 = PegNodeId(2, '2')
        id3 = PegNodeId(1, '999')

        assert id1 != id2
        assert id1 == id3

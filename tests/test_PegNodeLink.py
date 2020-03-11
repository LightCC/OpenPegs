import pytest
from src.PegNodeLink import PegNodeLink
from src.PegNode import PegNode

def fake_function():
    pass

## supply a node_arg for instantiating PegNodeLink objects
# that is not a PegNode object to trigger a ValueError exception
@pytest.fixture(params=[None,
                        1,
                        'string',
                        1.1,
                        ['list', 1],
                        {1: 'dict'},
                        {'set', 1, 2},
                        fake_function
                        ])
def node_arg(request):
    return request.param

class TestPegNodeLink:
    def test_init_raises_valueerror_if_arg_is_not_PegNode(self, node_arg):
        node1 = PegNode(None, 1)
        # No Exception should be raised
        PegNodeLink(node1, node1, node1)
        # Ensure bad first arg raises ValueError
        with pytest.raises(ValueError):
            PegNodeLink(node_arg, node1, node1)
        # Ensure bad second arg raises ValueError
        with pytest.raises(ValueError):
            PegNodeLink(node1, node_arg, node1)
        # Ensure bad third arg raises ValueError
        with pytest.raises(ValueError):
            PegNodeLink(node1, node1, node_arg)
    
    def test_PegNodeLink_string_output(self):
        node1 = PegNode(None, 1)
        node2 = PegNode(None, '2')
        node3 = PegNode(None, 3.14159)
        link1 = PegNodeLink(node1, node2, node3)
        assert str(link1) == '1->2->3.14159'
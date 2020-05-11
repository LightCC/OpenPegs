from src.pegs.PegNodeLink import PegNodeLink


def fake_function():
    pass


class TestPegNodeLink:

    def test_returning_all_nodes(self):
        # Setup
        link = PegNodeLink(1, 2, 3)

        assert link == (1, 2, 3)
        # Test node access methods
        assert link.start == 1
        assert link.adjacent == 2
        assert link.end == 3

    def test_PegNodeLink_string_output(self):
        link1 = PegNodeLink(1, 2, 3)
        assert str(link1) == '1->2->3'
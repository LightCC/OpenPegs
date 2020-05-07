import pytest
from src.pegs.PegNodePeg import PegNodePeg, PegNotAvailable, PegAlreadyPresent
from src.pegs.PegException import *


class TestPegNodePeg:

    def test_create_peg_object(self):
        peg_default = PegNodePeg()
        assert peg_default.peg == False
        assert str(peg_default) == 'o'
        peg_true = PegNodePeg(True)
        assert peg_true.peg == True
        assert str(peg_true) == 'x'

    def test_set_and_remove_pegs(self):
        peg = PegNodePeg()
        assert str(peg) == 'o'
        with pytest.raises(PegNotAvailable):
            peg.remove_peg()
        peg.add_peg()
        assert str(peg) == 'x'
        with pytest.raises(PegAlreadyPresent):
            peg.add_peg()
        peg.remove_peg()
        assert str(peg) == 'o'

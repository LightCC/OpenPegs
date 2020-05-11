from typing import Any, List, Tuple, Dict
from .PegException import *


class PegNodePeg:
    """Initialize PegNodePeg object

    Args:
        peg_is_present (Any, optional): Set `peg` property True if this value evaluates to True. Defaults to False.
    """
    peg_str = {False: 'o', True: 'x'}

    def __init__(self, peg_is_present: Any = False) -> None:
        self._peg = peg_is_present

    @property
    def is_present(self) -> bool:
        """State of peg - True is present, False is not present."""
        return self._peg

    @is_present.setter
    def is_present(self, peg: Any) -> None:
        """Set is_present to True if input evaluates to True"""
        self._peg = True if peg else False

    def add_peg(self):
        """Add a peg to this peg location

        Raises:
            PegAlreadyPresent: There is already a peg present, cannot add one
        """
        if self._peg:
            raise PegAlreadyPresent('Peg already present, cannot add')
        else:
            self._peg = True

    def remove_peg(self):
        """Remove the peg currently in this position

        Raises:
            PegNotAvailable: There is not a peg in this position to remove
        """
        if self._peg:
            self._peg = False
        else:
            raise PegNotAvailable('No peg was present to remove')

    def __str__(self):
        return self.peg_str[self._peg]

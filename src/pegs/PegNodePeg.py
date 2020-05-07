from typing import Any, List, Tuple, Dict
from .PegException import *


class PegNodePeg:
    """Initialize PegNodePeg object

    Args:
        peg_is_present (Any, optional): Set `peg` property True if this value evaluates to True. Defaults to False.
    """

    def __init__(self, peg_is_present: Any = False, peg_str_dict: Dict[bool, str] = None) -> None:
        self.peg = peg_is_present
        if peg_str_dict is None:
            self._peg_str = {False: 'o', True: 'x'}
        else:
            self._peg_str = self.validate_peg_str(peg_str_dict)

    @property
    def peg(self) -> bool:
        """State of peg - True is present, False is not present."""
        return self._peg

    @peg.setter
    def peg(self, peg: Any) -> None:
        """Set peg property to True if input evaluates to True"""
        self._peg = True if peg else False

    def validate_peg_str(self, peg_str_dict: Dict[bool, str]) -> Dict[bool, str]:
        """Set the peg string dictionary

        :param peg_str_dict: dict with the string to print for the corresponding peg state keys. Default: {False: 'o', True: 'x'}
        :type peg_str_dict: Dict[bool, str]
        """
        if not isinstance(peg_str_dict, dict):
            raise ValueError('_peg_str must be of type Dict[bool, str]')
        for peg_key, peg_value in peg_str_dict.items():
            if not isinstance(peg_key, bool):
                raise ValueError('peg_str_dict key in "{}: {}" must be bool, was {}'.format(peg_key, peg_value, type(peg_key)))
            if not isinstance(peg_value, str):
                raise ValueError('peg_str_dict value in "{}: {}" must be str, was {}'.format(peg_key, peg_value, type(peg_value)))
        return peg_str_dict

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
        return self._peg_str[self._peg]

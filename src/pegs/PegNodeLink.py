from typing import NamedTuple

class PegNodeLink(NamedTuple):
    '''PegNodeLink objects provide mapping of legal jumps from a PegNode

    When jumping, a PegNodeLink provides the start_node that a peg is currently located at, an adjacent_node that can be jumped over (if a peg is at that location), and an end_node (which must be empty) for the peg to land at after jumping.

    Arguments:
      start(int): Beginning Node Position
      adjacent(int): Adjacent Node that will be jumped over
      end(int): Ending Node that will be jumped to
    '''
    start: int
    adjacent: int
    end: int

    def __repr__(self):
        return f'{self.start}->{self.adjacent}->{self.end}'

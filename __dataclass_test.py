import dataclasses as dc
import typing as typ


@dc.dataclass(frozen=True)
class BoardId(object):
    peg0: bool = False
    peg1: bool = False
    peg2: bool = False
    peg3: bool = False

    @classmethod
    def make(cls, boardid=None):
        if boardid:
            return cls(*[True if x == 'x' else False for x in boardid])
        else:
            return cls()

    def __repr__(self):
        xo = ''.join(['x' if x else 'o' for x in dc.astuple(self)])
        return f'Id({xo})'


@dc.dataclass
class Link:
    start: int
    adjacent: int
    end: int

    def __repr__(self):
        return f'({self.start}->{self.adjacent}->{self.end})'


@dc.dataclass
class Move:
    move: Link = None
    board: BoardId = BoardId(True, True)


@dc.dataclass
class Chain:
    moves: typ.List[Move] = dc.field(default_factory=list)


if __name__ == "__main__":
    m1 = Move(Link(start=1, adjacent=2, end=3), BoardId.make('oxxo'))
    m2 = Move(Link(start=3, adjacent=2, end=1), BoardId.make('xxxo'))
    ch = Chain(moves=[m1, m2])
    print(f'ch = {ch}')
    print(f'ch.moves[0].move = {ch.moves[0].move}')
    print(f'ch.moves[0].board = {ch.moves[0].board}')

    print()

from typing import NamedTuple


class TicTacToe(NamedTuple):
    """A tic-tac-toe board, each character is ' ', 'x', 'o'"""
    row1: str = '   '
    row2: str = '   '
    row3: str = '   '

    @classmethod
    def make(cls, *args, **kwargs):
        print(f'Enter .make with {cls}, {args}, {kwargs}')
        if len(args) == 1 and args[0] == 0:
            new_args = ['   ', '   ', '   ']
        else:
            new_args = args
        self = cls(*new_args, *kwargs)
        return self


if __name__ == '__main__':
    a = TicTacToe.make('xo ', 'x x', 'o o')
    print(a)
    b = TicTacToe.make(0)
    print(b)

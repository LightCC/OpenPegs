# OpenPegs - Peg Hopper Game and Analysis package

Peg Hopper is a game where there is a geometric layout of peg holes. The game board is filled with pegs, generally allowing the player to choose one hole on the board to start with as empty (i.e. without a peg).

Play proceeds with the player jumping any peg over another peg, into an empty peg hole, removing the peg that was jumped from the board. The goal is to remove the pegs in a way that the remaining number of pegs is the least possible, generally to a single remaining peg on the board.

A classic version of the game had a board with a triangle or pyramid pattern, with 1 hole in the top row, 2 in the next, increasing by one until there are 5 in the bottom row. It is possible for the game to reduce to a single peg for a winning game with this pattern.

For example, if you take the board with pegs identified as below:
```
      1
     2 3
    4 5 6
   7 8 9 a
  b c d e f
```

and if the initial hole left open is hole 1, the board will look like the following, with `x` indicating a peg is present, and `o` indicating the peg is open:
```
      o
     x x
    x x x
   x x x x
  x x x x x
```

The the first move must be one of the following:
1. Jump peg 4 over peg 2, removing peg 2 and filling hole 1, leaving holes 2 and 4 open
```
      x
     o x
    o x x
   x x x x
  x x x x x
```

2. Jump peg 6 over peg 3, removing peg 3 and filling hole 1, leaving holes 3 and 6 open
```
      x
     x o
    x x o
   x x x x
  x x x x x
```

After either of these moves, there will be 4 possible moves to jump one of the remaining pegs over another peg into one of the empty holes.

Play proceeds until there are no pegs adjacent to each other. The remaining pegs on the board are counted to create the final score, with a lower score being better.

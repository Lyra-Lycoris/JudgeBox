# Tic-Tac-Toe Result

Two players alternately place their marks on a $3 \times 3$ tic-tac-toe board. The first player uses `X`, the second uses `O`, and nine marks are required to fill the board.

The cells are numbered as follows:

```
1 2 3
4 5 6
7 8 9
```

You are given the nine cell numbers in the order in which they are played (a permutation of $1 \sim 9$). Moves $1, 3, 5, 7, 9$ are played by `X`, and moves $2, 4, 6, 8$ by `O`.

Determine the move after which the game is first decided. Three marks in one line (the same row, column or diagonal) win the game. If all nine moves are played and nobody owns a line, the game is a draw. Moves that come after the game is decided are ignored.

### Input

One line with nine integers: the cell numbers in playing order, separated by single spaces.

### Output

One integer:

- $t$ ($1 \le t \le 9$) if someone completes a line for the first time after move $t$;
- `0` if all nine moves are played without any line.

### Constraints

The nine integers form a permutation of $1 \sim 9$, so no cell is ever played twice.

### Sample explanation

Sample 1: the playing order is `1 4 2 5 3 ...`; `X` occupies cells 1, 2 and 3, so the first row is completed after move 5.

Sample 2: `X` owns cells 1, 3, 4, 8, 9 and `O` owns 2, 5, 6, 7; after nine moves nobody has a line, so the answer is `0`.

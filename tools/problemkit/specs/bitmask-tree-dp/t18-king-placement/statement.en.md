# Placing Kings on a Board

You are given a board with $n$ rows and $m$ columns. Place **some kings** on the board; a king attacks the eight surrounding cells (horizontally, vertically and diagonally, staying inside the board).

No two kings may occupy the same cell, and no two kings may attack each other. Count the number of different placements. Placing no king at all (an empty board) is allowed and counts as one placement.

### Input

One line with two integers $n$ and $m$: the number of rows and columns.

### Output

One integer: the number of valid placements.

### Constraints

- $1 \le n, m \le 11$
- The largest answer ($11 \times 11$ board) is $60711713670028729$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3 3
```

**Output**

```
35
```

### Sample Explanation

On a $3 \times 3$ board:

- $0$ kings: $1$ placement;
- $1$ king: $9$ placements;
- $2$ kings: $16$ placements (choosing two cells that do not attack each other);
- $3$ kings: $8$ placements;
- $4$ kings: $1$ placement (the four corners);
- $5$ or more kings: impossible.

The total is $1 + 9 + 16 + 8 + 1 = 35$.

# Placing Kings with Bitmask DP

There is a board with $n$ rows and $m$ columns. Some cells of the board are broken and cannot hold a piece.

You have to place **any number of kings** (possibly zero) on the board so that no two kings attack each other. A king attacks the $8$ cells around it (horizontally, vertically and diagonally adjacent).

Count the number of placements modulo $10^9+7$.

### Input

The first line contains two integers $n$ and $m$.

The second line contains $n$ integers $b_1, b_2, \dots, b_n$; bit $j$ of $b_i$ ($0 \le j < m$, least significant bit is bit $0$) is $1$ if the cell in row $i$, column $j+1$ is broken, and $0$ otherwise.

### Output

A single line with one integer: the number of placements modulo $10^9+7$.

### Constraints

- $1 \le n \le 200$
- $1 \le m \le 9$
- $0 \le b_i < 2^m$
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=2,\ m=2$ and there is no broken cell:

```
. .
. .
```

On a $2 \times 2$ board every two cells attack each other (horizontally, vertically or diagonally), so at most one king can be placed:

- no king: $1$ placement;
- one king: $4$ placements (any of the $4$ cells).

In total $1 + 4 = 5$ placements, hence the output `5`.

### Hint

Use a row-by-row bitmask DP. Represent the kings of one row as an $m$-bit mask and first precompute the **row-valid** masks: no two kings may be horizontally adjacent, i.e.

$$s \ \&\ (s \ll 1) = 0 .$$

For $m \le 9$ there are only $89$ such masks. Two consecutive rows with masks $s$ (previous) and $t$ (current) are compatible iff

$$s \ \&\ t = 0,\qquad (s \ll 1) \ \&\ t = 0,\qquad (s \gg 1) \ \&\ t = 0,$$

which exclude vertical and diagonal attacks. The mask of the current row must also avoid the broken cells: $s \ \&\ b_i = 0$.

Let $dp[s]$ be the number of placements of the processed rows whose last row has mask $s$; transfer row by row. The complexity is $O(n \cdot V^2)$ with $V \le 89$.

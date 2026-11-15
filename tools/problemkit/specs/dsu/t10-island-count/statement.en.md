# Number of Islands

You are given an $n \times m$ grid; every cell is either `0` (water) or `1` (land).

Only the four orthogonal directions (up, down, left, right) count as adjacent; diagonal contact does not connect cells. A maximal group of `1` cells connected through orthogonal adjacency is called an island. Count the islands in the grid.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- Each of the next $n$ lines contains $m$ integers (only `0` or `1`), separated by single spaces.

### Output

One line with a single integer: the number of islands.

### Constraints

$1 \le n, m \le 500$.

The grid contains only `0` and `1`.

### Sample explanation

Sample 1: $n = 4$, $m = 5$ and the grid is

```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

- The four `1` cells in the upper-left $2 \times 2$ block touch orthogonally and form island $1$.
- The `1` at row $3$, column $3$ is surrounded by water and forms island $2$ by itself.
- The two `1` cells at row $4$, columns $4$ and $5$ touch horizontally and form island $3$.

Hence the answer is $3$.

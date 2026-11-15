# Number of Islands

You are given an $n \times m$ matrix of `0`s and `1`s, where `1` means land and `0` means water.

An island is a maximal set of `1` cells connected through **four-directional** adjacency (up, down, left, right; diagonal adjacency does not connect). Count the islands in the matrix.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $n$ lines each contain $m$ integers (`0` or `1`) separated by single spaces.

### Output

Print one integer: the number of islands.

### Constraints

- $1 \le n, m \le 500$
- Every cell is either `0` or `1`
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

**Output**

```
3
```

### Sample explanation

The matrix is:

```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

- The four `1`s in the top-left $2 \times 2$ block are connected, giving island 1;
- the `1` at row 3, column 3 is surrounded by `0`s, giving island 2;
- the last two `1`s of row 4 touch horizontally, giving island 3.

So the answer is `3`.

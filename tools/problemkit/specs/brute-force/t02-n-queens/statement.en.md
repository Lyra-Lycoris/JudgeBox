# Counting N-Queens Solutions

Place $n$ queens on an $n \times n$ chessboard so that no two queens attack each other: no two queens may share a row, a column, or a diagonal.

Count the number of distinct placements.

### Input

A single line with one integer $n$.

### Output

Print a single integer: the number of placements.

### Constraints

- $1 \le n \le 10$
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4
```

**Output**

```
2
```

### Sample explanation

For $n = 4$ there are exactly $2$ placements:

```
. Q . .        . . Q .
. . . Q        Q . . .
Q . . .        . . . Q
. . Q .        . Q . .
```

so the output is `2`.

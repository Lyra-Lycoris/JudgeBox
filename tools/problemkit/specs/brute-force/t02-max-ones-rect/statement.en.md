# Largest All-Ones Subrectangle

Given an $n \times m$ matrix of zeros and ones, find a subrectangle (a contiguous block of rows together with a contiguous block of columns) that contains only `1`s and has the largest possible area, measured in cells.

If the matrix contains no `1` at all, the answer is $0$.

### Input

The first line contains two integers $n$ and $m$, separated by a space.

Each of the next $n$ lines contains $m$ integers, either `0` or `1`, separated by spaces.

### Output

Print a single integer: the area of the largest all-ones subrectangle.

### Constraints

- $1 \le n, m \le 60$
- Every matrix entry is either $0$ or $1$
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3 4
1 0 1 1
1 0 1 1
1 1 1 1
```

**Output**

```
6
```

### Sample explanation

The sample matrix is

```
1 0 1 1
1 0 1 1
1 1 1 1
```

Columns $2$ and $3$ are filled with `1` in all three rows, forming a $3 \times 2$ all-ones subrectangle of area $6$. No larger all-ones subrectangle exists, so the output is `6`.

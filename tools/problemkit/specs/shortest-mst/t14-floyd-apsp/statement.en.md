# All-Pairs Shortest Paths (Floyd)

You are given a **directed** graph with $n$ vertices in adjacency-matrix form: $w_{i,j}$ is the weight of the direct edge from $i$ to $j$, and $w_{i,j} = -1$ means there is no such edge. It is guaranteed that $w_{i,i} = 0$.

Compute the shortest distance between every ordered pair of vertices.

### Input

The first line contains one integer $n$.

Each of the next $n$ lines contains $n$ integers: the matrix $w$.

### Output

Print one line with $n^2$ integers, in **row-major** order: the value at position $(i, j)$ (1-based) is the shortest distance from $i$ to $j$, or $-1$ if $j$ is unreachable from $i$.

### Constraints

- $1 \le n \le 300$
- $w_{i,i} = 0$
- For $i \ne j$: $w_{i,j} = -1$ means no direct edge, otherwise $0 \le w_{i,j} \le 10^9$
- There are no negative edge weights, and every shortest distance is at most $3 \times 10^{11}$
- Time limit 3000 ms, memory limit 256 MB

### Sample

**Input**

```
4
0 3 -1 7
-1 0 2 -1
-1 -1 0 1
-1 -1 -1 0
```

**Output**

```
0 3 5 6 -1 0 2 3 -1 -1 0 1 -1 -1 -1 0
```

### Sample explanation

The edges are: $1 \to 2$ ($3$), $1 \to 4$ ($7$), $2 \to 3$ ($2$), $3 \to 4$ ($1$).

- $1 \to 3$ via $1 \to 2 \to 3$ has length $3 + 2 = 5$;
- $1 \to 4$ via $1 \to 2 \to 3 \to 4$ has length $3 + 2 + 1 = 6$, better than the direct edge of weight $7$;
- $2 \to 4$ has length $2 + 1 = 3$;
- vertex $4$ has no outgoing edges, so the fourth row is all $-1$ except $d_{4,4} = 0$.

Row-major output gives exactly the line shown above.

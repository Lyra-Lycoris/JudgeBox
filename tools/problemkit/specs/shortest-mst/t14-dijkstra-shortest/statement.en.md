# Single Source Shortest Path (Dijkstra)

You are given a **directed** graph with $n$ vertices and $m$ edges; every edge length is a non-negative integer. Given a source vertex $s$, compute the shortest distance from $s$ to every vertex.

If a vertex $t$ is unreachable from $s$, its distance is defined to be $-1$.

### Input

The first line contains three integers $n$, $m$ and $s$, separated by spaces.

Each of the next $m$ lines contains three integers $u$, $v$ and $w$, meaning a directed edge from $u$ to $v$ with length $w$.

### Output

Print one line with $n$ integers. The $i$-th integer is the shortest distance from $s$ to vertex $i$, or $-1$ if vertex $i$ is unreachable.

### Constraints

- $1 \le n \le 200000$, $0 \le m \le 200000$
- $1 \le u, v, s \le n$
- $0 \le w \le 10^9$
- Multiple edges and self-loops are allowed
- Every shortest distance from the source is at most $2 \times 10^{14}$, which fits in a signed 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4 5 1
1 2 2
1 3 5
2 3 1
2 4 6
3 4 2
```

**Output**

```
0 2 3 5
```

### Sample explanation

Starting from vertex $1$:

- vertex $1$ is at distance $0$;
- vertex $2$ is reached directly by $1 \to 2$, distance $2$;
- vertex $3$ is reached by $1 \to 2 \to 3$ with distance $2 + 1 = 3$, better than $1 \to 3$ with distance $5$;
- vertex $4$ is reached by $1 \to 2 \to 3 \to 4$ with distance $2 + 1 + 2 = 5$, better than $1 \to 2 \to 4$ with distance $8$.

So the output is `0 2 3 5`.

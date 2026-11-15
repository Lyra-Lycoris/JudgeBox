# Negative Cycle Detection (Bellman-Ford)

You are given a **directed** graph with $n$ vertices and $m$ edges whose weights may be negative, plus a source vertex $s$.

Determine whether the graph contains a negative-weight cycle (a cycle whose total edge weight is negative) that is **reachable from $s$**.

Only negative cycles reachable from $s$ can change shortest paths, so unreachable negative cycles must not be counted.

### Input

The first line contains three integers $n$, $m$ and $s$, separated by spaces.

Each of the next $m$ lines contains three integers $u$, $v$ and $w$: a directed edge from $u$ to $v$ with weight $w$.

### Output

Print `YES` if some negative-weight cycle is reachable from $s$, otherwise print `NO`.

### Constraints

- $1 \le n \le 500$, $0 \le m \le 2000$
- $1 \le u, v, s \le n$
- $|w| \le 10^9$
- Multiple edges and self-loops are allowed (a self-loop $u \to u$ with negative weight is itself a negative cycle)
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4 4 1
1 2 1
2 3 -3
3 4 1
4 2 -1
```

**Output**

```
YES
```

### Sample explanation

Starting from vertex $1$, the edge $1 \to 2$ leads into the cycle $2 \to 3 \to 4 \to 2$. Its total weight is

$$(-3) + 1 + (-1) = -3 < 0,$$

so this negative cycle is reachable from $s = 1$ and the answer is `YES`.

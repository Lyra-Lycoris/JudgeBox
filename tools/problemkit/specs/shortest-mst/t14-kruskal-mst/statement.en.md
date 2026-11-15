# Minimum Spanning Tree (Kruskal)

You are given a **connected undirected** graph with $n$ vertices and $m$ edges. Compute the total weight of its minimum spanning tree (MST): a set of $n-1$ edges that connects all vertices with the smallest possible sum of weights.

### Input

The first line contains two integers $n$ and $m$, separated by a space.

Each of the next $m$ lines contains three integers $u$, $v$ and $w$: an undirected edge between $u$ and $v$ with weight $w$.

### Output

Print one integer: the total weight of the minimum spanning tree.

### Constraints

- $1 \le n \le 200000$, $0 \le m \le 200000$
- $1 \le u, v \le n$, $|w| \le 10^9$
- The graph is connected whenever $n \ge 2$; for $n = 1$ there are no edges and the answer is $0$
- Multiple edges and self-loops are allowed
- The answer is at most $2 \times 10^{14}$, which fits in a signed 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4 5
1 2 1
1 3 4
2 3 2
2 4 5
3 4 3
```

**Output**

```
6
```

### Sample explanation

Taking edges $1-2$ ($1$), $2-3$ ($2$) and $3-4$ ($3$) connects all four vertices with total weight

$$1 + 2 + 3 = 6.$$

No connected spanning subgraph is cheaper (for instance, replacing $3-4$ by $2-4$ of weight $5$ gives $1+2+5=8$), so the answer is `6`.

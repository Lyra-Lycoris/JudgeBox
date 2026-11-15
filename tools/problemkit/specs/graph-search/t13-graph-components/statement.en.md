# Counting Connected Components

You are given an undirected graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. Count its connected components.

An isolated vertex (a vertex with no incident edge) forms a connected component by itself. Self-loops ($u = v$) and multiple edges are allowed.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $m$ lines each contain two integers $u$ and $v$, separated by a single space, meaning there is an undirected edge between vertex $u$ and vertex $v$.

When $m = 0$, nothing follows the first line.

### Output

Print one integer: the number of connected components.

### Constraints

- $1 \le n \le 200000$
- $0 \le m \le 200000$
- $1 \le u, v \le n$
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
5 3
1 2
2 3
4 5
```

**Output**

```
2
```

### Sample explanation

Vertices $1, 2, 3$ form one component and vertices $4, 5$ form another. Every vertex is covered, so there are $2$ connected components.

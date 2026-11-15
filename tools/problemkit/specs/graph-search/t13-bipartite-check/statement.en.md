# Bipartite Graph Check

You are given an undirected graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. Decide whether it is bipartite.

A graph is bipartite if its vertices can be split into two sets $A$ and $B$ such that every edge has one endpoint in $A$ and the other in $B$ (equivalently, the graph contains no cycle of odd length).

Self-loops ($u = v$) and multiple edges are allowed.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $m$ lines each contain two integers $u$ and $v$, separated by a single space, meaning there is an undirected edge between vertex $u$ and vertex $v$.

When $m = 0$, nothing follows the first line.

### Output

Print one line: `YES` if the graph is bipartite, otherwise `NO`.

### Constraints

- $1 \le n \le 200000$
- $0 \le m \le 200000$
- $1 \le u, v \le n$
- Time limit 2000 ms, memory limit 256 MB

### Samples

**Input 1**

```
4 4
1 2
2 3
3 4
4 1
```

**Output 1**

```
YES
```

**Input 2**

```
3 3
1 2
2 3
3 1
```

**Output 2**

```
NO
```

### Sample explanation

Sample 1: $1-2-3-4-1$ is a cycle of length $4$. Taking $A = \{1, 3\}$ and $B = \{2, 4\}$ works, so the answer is `YES`.

Sample 2: the three vertices are pairwise connected, forming a triangle (an odd cycle of length $3$). Whatever split into two sets you choose, one edge has both endpoints in the same set, so the answer is `NO`.

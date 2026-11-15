# Cycle Detection in a Directed Graph

You are given a directed graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. Decide whether the graph contains a cycle, and count **how many vertices lie on at least one directed cycle**.

If the graph has no cycle at all, the answer is $0$.

A vertex $v$ lies on a cycle if there is a directed path starting at $v$, using at least one edge, that comes back to $v$. A self-loop $u \to u$ counts as a cycle of length $1$. Multiple edges do not change the answer.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $m$ lines each contain two integers $u$ and $v$, separated by a single space, meaning there is a directed edge from $u$ to $v$.

When $m = 0$, nothing follows the first line.

### Output

Print one integer: the number of vertices that lie on at least one directed cycle.

### Constraints

- $1 \le n \le 200000$
- $0 \le m \le 200000$
- $1 \le u, v \le n$
- Time limit 2000 ms, memory limit 256 MB

### Samples

**Input 1**

```
6 5
1 2
2 3
3 1
4 5
5 6
```

**Output 1**

```
3
```

**Input 2**

```
2 1
1 1
```

**Output 2**

```
1
```

### Sample explanation

Sample 1: $1 \to 2 \to 3 \to 1$ is a directed cycle, so vertices $1, 2, 3$ lie on it; $4 \to 5 \to 6$ is only a chain that never returns, so $4, 5, 6$ do not lie on any cycle. The answer is `3`.

Sample 2: $1 \to 1$ is a self-loop, so vertex $1$ lies on a cycle; vertex $2$ has no edges. The answer is `1`.

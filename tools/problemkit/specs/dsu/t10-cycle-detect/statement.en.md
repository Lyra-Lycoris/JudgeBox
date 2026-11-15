# Cycle Detection in an Undirected Graph

You are given an undirected graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. Determine whether the graph contains a cycle.

The graph is guaranteed to be simple: no self-loops and no multiple edges between the same pair of vertices.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- Each of the next $m$ lines contains two integers $u_i$ and $v_i$, meaning there is an edge between vertex $u_i$ and vertex $v_i$.

### Output

Print `YES` on a single line if the graph contains a cycle, otherwise print `NO`.

### Constraints

$1 \le n \le 200000$, $0 \le m \le 200000$, $1 \le u_i, v_i \le n$, $u_i \ne v_i$.

No pair of vertices is given twice, and no self-loop $(u, u)$ appears.

### Sample explanation

Sample 1: $n = 4$, $m = 4$, with edges $(1,2)$, $(2,3)$, $(3,4)$, $(4,1)$. Starting at vertex $1$ you can walk $1 \to 2 \to 3 \to 4 \to 1$ back to vertex $1$. This closed walk of length $4$ is a cycle, so the answer is `YES`.

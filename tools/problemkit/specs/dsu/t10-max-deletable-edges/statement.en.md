# Maximum Number of Removable Edges

You are given an undirected graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. The graph may be disconnected and may contain multiple edges, but it has no self-loops.

You may delete some edges. After the deletion, the following must hold: for any two vertices that were mutually reachable in the original graph, they are still mutually reachable in the remaining graph. In other words, every original connected component must stay connected as a whole.

Find the maximum number of edges you can delete.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- Each of the next $m$ lines contains two integers $u_i$ and $v_i$, meaning there is an edge between vertex $u_i$ and vertex $v_i$.

### Output

One line with a single integer: the maximum number of edges that can be deleted.

### Constraints

$1 \le n \le 200000$, $0 \le m \le 200000$, $1 \le u_i, v_i \le n$, $u_i \ne v_i$.

Multiple edges are allowed and the graph need not be connected.

### Sample explanation

Sample 1: $n = 4$, $m = 5$ with edges $(1,2)$, $(2,3)$, $(3,1)$, $(1,2)$, $(3,4)$.

All four vertices are mutually reachable, and the graph must stay connected after the deletion, so at least $n - 1 = 3$ edges must remain (for example $(1,2)$, $(2,3)$, $(3,4)$). There were $5$ edges, so at most $5 - 3 = 2$ edges can be deleted.

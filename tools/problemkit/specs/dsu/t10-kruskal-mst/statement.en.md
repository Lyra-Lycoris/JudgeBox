# Minimum Spanning Tree Weight

You are given a weighted undirected graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. Multiple edges are allowed, there are no self-loops, and the graph is not guaranteed to be connected.

Choose a set of edges that connects **all** vertices (that is, a spanning tree) while minimizing the total edge weight. Output that minimum total weight.

If the graph is disconnected no spanning tree exists, so output `-1`. In particular, when $n = 1$ no edge is needed and the answer is $0$.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- Each of the next $m$ lines contains three integers $u_i, v_i, w_i$: an edge between vertex $u_i$ and vertex $v_i$ with weight $w_i$.

### Output

One line with a single integer: the minimum total weight of a spanning tree, or `-1` if the graph is disconnected.

### Constraints

$1 \le n \le 200000$, $0 \le m \le 200000$, $1 \le u_i, v_i \le n$, $u_i \ne v_i$, $-10^9 \le w_i \le 10^9$.

Weights may be negative, multiple edges are allowed, and the graph need not be connected.

### Sample explanation

Sample 1: $n = 4$, $m = 5$ with edges $(1,2,1)$, $(2,3,2)$, $(3,4,3)$, $(1,4,5)$, $(1,3,4)$.

Taking $(1,2,1)$, $(2,3,2)$ and $(3,4,3)$ connects all four vertices with total weight $1 + 2 + 3 = 6$.

Replacing $(3,4,3)$ by $(1,4,5)$ would give total weight $8$, which is worse; no other choice is better. So the minimum total weight is $6$.

# Number of Connected Components

You are given an undirected graph with $n$ vertices (numbered $1 \sim n$) and $m$ edges. The graph may contain multiple edges between the same pair of vertices, but it has no self-loops.

Two vertices belong to the same connected component if one can be reached from the other by following edges; an isolated vertex is a component by itself. Count the number of connected components of the whole graph.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- Each of the next $m$ lines contains two integers $u_i$ and $v_i$, meaning there is an edge between vertex $u_i$ and vertex $v_i$.

### Output

One line with a single integer: the number of connected components.

### Constraints

$1 \le n \le 200000$, $0 \le m \le 200000$, $1 \le u_i, v_i \le n$, $u_i \ne v_i$.

Multiple edges are allowed, i.e. the same pair may be given more than once.

### Sample explanation

Sample 1: $n = 5$, $m = 2$, with edges $(1,2)$ and $(2,3)$.

- Vertices $1, 2, 3$ are connected by the edges and form the component $\{1,2,3\}$.
- Vertex $4$ has no edge, so it forms $\{4\}$ on its own.
- Vertex $5$ has no edge, so it forms $\{5\}$ on its own.

Hence there are $3$ connected components.

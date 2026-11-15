# Orient an Undirected Graph

You are given an undirected simple graph with $n$ vertices and $m$ edges (no self-loops, no multi-edges). You may assign a direction to every edge, turning it into a directed edge.

Find an orientation such that **the in-degree of every vertex is at most $1$**; if no such orientation exists, report that it is impossible.

Having in-degree at most $1$ means that the resulting directed graph consists of several directed paths and directed cycles: every vertex has at most one incoming edge (a vertex with in-degree $0$ is the start of a directed path).

### Input

- The first line contains two integers $n$ and $m$.
- Each of the next $m$ lines contains two integers $u_i, v_i$, describing the $i$-th undirected edge.

### Output

- If a valid orientation exists, print $2m$ space-separated integers. In input order, for the $i$-th edge print two integers $a_i, b_i$ meaning that this edge is directed as $a_i \to b_i$. Here $(a_i, b_i)$ must be either $(u_i, v_i)$ or $(v_i, u_i)$.
- If no valid orientation exists, print a single integer `-1`.

This problem uses a **special judge**, so any valid orientation is accepted.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $0 \le m \le 2 \times 10^5$
- $1 \le u_i \ne v_i \le n$; the graph has no self-loops and no multi-edges

### Sample explanation

Sample 1: $n = 4$, $m = 4$ with edges $1-2$, $2-3$, $3-1$, $3-4$.

The output `2 1 3 2 1 3 3 4` directs the four edges as $2 \to 1$, $3 \to 2$, $1 \to 3$, $3 \to 4$.

The in-degrees are: vertex $1$ from $2$, vertex $2$ from $3$, vertex $3$ from $1$, vertex $4$ from $3$ — all equal to $1$, so every in-degree is at most $1$ and the answer is valid. (Any valid orientation is accepted; for instance `1 2 2 3 3 1 3 4` is equally correct.)

### Hint

For a connected component with $V$ vertices and $E$ edges, the sum of all in-degrees after orienting equals $E$, and every in-degree is at most $1$, so $E \le V$ is necessary. On the other hand a connected component needs at least $V-1$ edges, hence $E \ge V-1$. Therefore every component must be either a **tree** ($E = V-1$) or a **unicyclic graph** ($E = V$); if some component has $E > V$, the answer is `-1`.

Construction: run an iterative DFS on every component to obtain a spanning tree.

- Orient every tree edge from parent to child. Then the root has in-degree $0$ and every other vertex has exactly one incoming edge.
- In a unicyclic component there is exactly one non-tree edge (a back edge). Orient it from the **deeper endpoint to the shallower endpoint**; together with the tree edges of the cycle this forms a directed cycle, and every vertex on the cycle gets in-degree exactly $1$.
- If the "top" vertex of the cycle is not the DFS root, the tree edges on the short "stem" from the root down to the cycle top must be **reversed** (child to parent); otherwise the cycle top would receive an incoming edge from the stem in addition to the back edge and its in-degree would become $2$.

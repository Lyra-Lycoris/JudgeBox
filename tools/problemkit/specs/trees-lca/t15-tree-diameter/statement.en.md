# Tree Diameter

You are given an undirected tree with $n$ nodes numbered $1 \sim n$. Every edge has length $1$.

The distance between two nodes is the number of edges on the unique simple path connecting them. The **diameter** of a tree is the maximum distance over all pairs of nodes. Compute the diameter of the given tree.

### Input

The first line contains an integer $n$.

Each of the following $n-1$ lines contains two integers $u_i, v_i$, describing an edge between node $u_i$ and node $v_i$. These lines are absent when $n = 1$.

The input graph is guaranteed to be a tree on nodes $1 \sim n$.

### Output

One integer: the diameter, i.e. the number of edges on the longest path. The answer is $0$ when $n = 1$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le u_i, v_i \le n$
- All edge lengths are $1$; the graph is connected and acyclic

### Sample Explanation

The sample tree has $6$ nodes with edges $(1,2), (2,3), (3,4), (2,5), (5,6)$.

The farthest pair is $4$ and $6$: the path is $4 \to 3 \to 2 \to 5 \to 6$, using $4$ edges. Every other pair is at distance at most $4$, so the diameter is $4$.

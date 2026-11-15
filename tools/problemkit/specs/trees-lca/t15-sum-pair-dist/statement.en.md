# Sum of All Pairwise Distances

You are given an undirected tree with $n$ nodes numbered $1 \sim n$. Every edge has length $1$.

The distance $\mathrm{dist}(u, v)$ is the number of edges on the unique simple path between $u$ and $v$. Compute the sum of distances over all **unordered pairs** of nodes:

$$\sum_{1 \le u < v \le n} \mathrm{dist}(u, v).$$

### Input

The first line contains an integer $n$.

Each of the following $n-1$ lines contains two integers $u_i, v_i$ describing an edge. These lines are absent when $n = 1$.

The edges are guaranteed to form a tree.

### Output

One integer: the sum of distances over all unordered pairs. The answer is $0$ when $n = 1$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le u_i, v_i \le n$
- All edge lengths are $1$

### Sample Explanation

The sample is the chain $1 - 2 - 3$. Its three unordered pairs have distances:

- $\mathrm{dist}(1,2) = 1$
- $\mathrm{dist}(2,3) = 1$
- $\mathrm{dist}(1,3) = 2$

The total is $1 + 1 + 2 = 4$.

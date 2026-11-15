# Tree Centroid Index

You are given an undirected tree with $n$ nodes numbered $1 \sim n$.

Node $v$ is called a **centroid** of the tree if, after removing $v$ and all edges incident to it, every remaining connected component has at most $\lfloor n/2 \rfloor$ nodes. Equivalently, the largest component after removing $v$ contains at most $n/2$ nodes.

Every tree has at least one centroid and at most two. Output the **smallest index** among all centroids.

### Input

The first line contains an integer $n$.

Each of the following $n-1$ lines contains two integers $u_i, v_i$ describing an edge. These lines are absent when $n = 1$.

The edges are guaranteed to form a tree.

### Output

One integer: the smallest index of a centroid.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le u_i, v_i \le n$

### Sample Explanation

The sample is the chain $1 - 2 - 3 - 4 - 5 - 6$.

Removing $3$ leaves components $\{1,2\}$ and $\{4,5,6\}$, the largest having $3 \le 6/2 = 3$ nodes, so $3$ is a centroid. By symmetry $4$ is also a centroid. Removing any other node leaves a component with more than $3$ nodes. Hence the centroids are $3$ and $4$, and the smallest index is $3$.

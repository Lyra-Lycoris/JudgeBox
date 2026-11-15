# Lowest Common Ancestor (Binary Lifting)

You are given a tree with $n$ nodes numbered $1 \sim n$, rooted at node $1$. For two nodes $u, v$, their **lowest common ancestor** (LCA) is the deepest node that is an ancestor of both $u$ and $v$. A node counts as an ancestor of itself, so the LCA of $u$ and $u$ is $u$.

Answer $q$ queries; each query gives two nodes $u, v$ and asks for their LCA.

### Input

The first line contains an integer $n$.

Each of the following $n-1$ lines contains two integers $u_i, v_i$ describing a tree edge. These lines are absent when $n = 1$.

The next line contains an integer $q$.

Each of the following $q$ lines contains two integers $u, v$ describing one query.

The edges are guaranteed to form a tree rooted at $1$, and all query nodes lie in $1 \sim n$.

### Output

Print one line with $q$ space-separated integers; the $t$-th one is the answer to the $t$-th query.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 2 \times 10^5$
- $1 \le u, v, u_i, v_i \le n$

### Sample Explanation

The sample tree: node $1$ has children $2, 3$; node $2$ has children $4, 5$; node $3$ has child $6$; node $6$ has child $7$.

- Query $(4, 5)$: both have parent $2$, so the LCA is $2$.
- Query $(5, 7)$: $5$ lies in the subtree of $2$ and $7$ in the subtree of $3$, so they only share the root; the LCA is $1$.
- Query $(6, 7)$: $6$ is the parent of $7$, so the LCA is $6$.
- Query $(4, 4)$: a node is its own ancestor, so the LCA is $4$.

Hence the four answers are $2, 1, 6, 4$ and the output is `2 1 6 4`.

# Minimum Vertex Cover on a Tree

You are given a rooted tree with $n$ nodes numbered $1 \sim n$; node $1$ is the root.

A set of nodes is a **vertex cover** if every edge has at least one endpoint in the set. Find the minimum size of a vertex cover, i.e. the fewest nodes you must select.

### Input

The first line contains one integer $n$.

The second line contains $n-1$ integers $p_2, p_3, \dots, p_n$, where $p_i$ is the parent of node $i$ and $1 \le p_i < i$. When $n=1$ this line is empty (nothing is read).

### Output

One integer: the minimum vertex cover size. For $n=1$ there are no edges, so the answer is $0$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- For every $2 \le i \le n$, $1 \le p_i < i$ (so node $1$ is the root and the input is always a tree)
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
5
1 1 3 3
```

**Output**

```
2
```

### Sample Explanation

The tree has $4$ edges: $(1,2)$, $(1,3)$, $(3,4)$, $(3,5)$.

- Choosing $\{1, 3\}$ covers every edge: each edge has at least one chosen endpoint, so it is a valid vertex cover of size $2$;
- One node is not enough: choosing $1$ misses $(3,4)$, choosing $3$ misses $(1,2)$, and any other single node misses even more.

Therefore the minimum vertex cover size is $2$.

# Sum of Distances from Every Node

You are given a tree with $n$ nodes numbered $1 \sim n$; node $1$ is the root. Every edge has length $1$.

For each node $v$, let $f(v) = \sum_{u=1}^{n} \operatorname{dist}(v, u)$, the sum of distances from $v$ to all nodes (including itself, at distance $0$). Compute $f(1), f(2), \dots, f(n)$.

### Input

The first line contains one integer $n$.

The second line contains $n-1$ integers $p_2, p_3, \dots, p_n$, where $p_i$ is the parent of node $i$ and $1 \le p_i < i$. When $n=1$ this line is empty (nothing is read).

### Output

One line with $n$ integers; the $i$-th one is $f(i)$, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- For every $2 \le i \le n$, $1 \le p_i < i$ (so node $1$ is the root and the input is always a tree)
- Every $f(v)$ is at most $\frac{n(n-1)}{2} = 2 \times 10^{10}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
5
1 1 3 3
```

**Output**

```
6 9 5 8 8
```

### Sample Explanation

The tree is: children of $1$ are $2, 3$; children of $3$ are $4, 5$.

- $f(1) = 1 + 1 + 2 + 2 = 6$ (distances to $2,3,4,5$);
- $f(2) = 1 + 2 + 3 + 3 = 9$;
- $f(3) = 1 + 2 + 1 + 1 = 5$;
- $f(4) = 2 + 3 + 1 + 2 = 8$;
- $f(5) = 2 + 3 + 1 + 2 = 8$.

If the value for a node is known, the value for its child can be obtained by **rerooting**: with $s_v$ the size of the subtree rooted at $v$,

$$f(\text{son}) = f(v) + n - 2 s_{\text{son}}$$

For example $f(3) = f(1) + 5 - 2 \times 3 = 6 - 1 = 5$.

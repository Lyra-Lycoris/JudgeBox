# Subtree Size Statistics

You are given a rooted tree with $n$ nodes numbered $1 \sim n$, rooted at node $1$. The tree is described by a parent array: for every $i \ge 2$, the parent of node $i$ is $p_i$, with $1 \le p_i < i$.

The **subtree** of node $v$ consists of $v$ itself and every node having $v$ as an ancestor, i.e. all nodes reachable by going downwards from $v$. The subtree size is the number of nodes in it.

For every $1 \le v \le n$, compute the subtree size of node $v$.

### Input

The first line contains an integer $n$.

The second line contains $n-1$ integers $p_2, p_3, \dots, p_n$, the parents of nodes $2, 3, \dots, n$. This line is empty (and may be omitted) when $n = 1$.

It is guaranteed that $1 \le p_i < i$, so the input always describes a rooted tree with root $1$.

### Output

One line with $n$ space-separated integers; the $v$-th one is the subtree size of node $v$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le p_i < i$ for $2 \le i \le n$

### Sample Explanation

Here $n = 5$ with $p_2 = 1,\ p_3 = 1,\ p_4 = 2,\ p_5 = 2$.

Thus node $1$ has children $2, 3$ and node $2$ has children $4, 5$. The subtrees are:

- node $1$: $\{1,2,3,4,5\}$, size $5$;
- node $2$: $\{2,4,5\}$, size $3$;
- node $3$: $\{3\}$, size $1$;
- node $4$: $\{4\}$, size $1$;
- node $5$: $\{5\}$, size $1$.

So the output is `5 3 1 1 1`.

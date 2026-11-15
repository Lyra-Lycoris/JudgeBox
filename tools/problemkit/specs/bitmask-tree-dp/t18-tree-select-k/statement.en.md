# Choose k Nodes in a Tree

You are given a rooted tree with $n$ nodes numbered $1 \sim n$; node $1$ is the root. Node $i$ has weight $w_i$ (weights may be negative).

You must choose **exactly $k$ nodes** with the following rule: if a node is chosen, its parent must also be chosen (node $1$ has no parent, so it is exempt from this rule). Maximize the total weight of the chosen nodes.

Because node $1$ is an ancestor of every other node, any valid choice for $k \ge 1$ must contain node $1$.

### Input

The first line contains two integers $n$ and $k$.

The second line contains $n$ integers $w_1, w_2, \dots, w_n$.

The third line contains $n-1$ integers $p_2, p_3, \dots, p_n$, where $p_i$ is the parent of node $i$ and $1 \le p_i < i$. When $n=1$ this line is empty (nothing is read).

### Output

One integer: the maximum total weight of exactly $k$ chosen nodes.

### Constraints

- $1 \le n \le 3000$
- $1 \le k \le \min(n, 200)$
- $|w_i| \le 10^9$
- For every $2 \le i \le n$, $1 \le p_i < i$ (so node $1$ is the root and the input is always a tree)
- The absolute value of the answer is at most $3 \times 10^{12}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
6 3
4 -1 7 2 5 -3
1 1 2 3 3
```

**Output**

```
16
```

### Sample Explanation

The tree is: children of $1$ are $2, 3$; the child of $2$ is $4$; children of $3$ are $5, 6$. Weights: $w_1=4$, $w_2=-1$, $w_3=7$, $w_4=2$, $w_5=5$, $w_6=-3$.

Choosing exactly $3$ nodes with the "parent must be chosen too" rule:

- $\{1,3,5\}$: $4 + 7 + 5 = 16$, valid;
- $\{1,2,3\}$: $4 + (-1) + 7 = 10$, valid;
- $\{1,3,6\}$: $4 + 7 + (-3) = 8$, valid;
- $\{1,3,4\}$ is invalid, because the parent of $4$ (node $2$) is not chosen.

The maximum total weight is $16$.

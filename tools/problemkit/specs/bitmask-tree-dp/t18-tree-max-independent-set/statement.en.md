# Maximum Weight Independent Set on a Tree

You are given a rooted tree with $n$ nodes numbered $1 \sim n$; node $1$ is the root. Node $i$ has weight $w_i$ (weights may be negative).

A set of nodes is called **independent** if no two of its nodes are directly connected by an edge. Find an independent set whose total weight is as large as possible. The empty set is allowed (its total weight is $0$).

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $w_1, w_2, \dots, w_n$.

The third line contains $n-1$ integers $p_2, p_3, \dots, p_n$, where $p_i$ is the parent of node $i$ and $1 \le p_i < i$. When $n=1$ this line is empty (nothing is read).

### Output

One integer: the maximum total weight.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $|w_i| \le 10^9$
- For every $2 \le i \le n$, $1 \le p_i < i$ (so node $1$ is the root and the input is always a tree)
- The answer is at most $2 \times 10^{14}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
6
3 -2 5 4 -1 2
1 1 2 2 4
```

**Output**

```
9
```

### Sample Explanation

The tree is: children of $1$ are $2, 3$; children of $2$ are $4, 5$; the child of $4$ is $6$.

Weights: $w_1=3$, $w_2=-2$, $w_3=5$, $w_4=4$, $w_5=-1$, $w_6=2$.

- Taking $\{3, 4\}$ gives $5 + 4 = 9$; $3$ and $4$ are not adjacent, so it is valid;
- Taking $\{1, 4\}$ gives $3 + 4 = 7$;
- Taking $\{3, 6\}$ gives $5 + 2 = 7$;
- Taking all positive nodes $\{1, 3, 4, 6\}$ is invalid, because $1$ is adjacent to $3$ and $4$ is adjacent to $6$.

The maximum total weight is $9$.

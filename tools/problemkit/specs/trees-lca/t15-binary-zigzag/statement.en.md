# Zigzag Level Order of a Binary Tree

You are given a binary tree with $n$ nodes numbered $1 \sim n$, rooted at node $r$. The left and right children of each node are given as two integers, where $0$ means that the child does not exist.

Output all nodes in **zigzag** order:

- level $0$ (the root) is printed left to right;
- level $1$ is printed right to left;
- level $2$ is printed left to right;
- level $3$ is printed right to left;
- and so on, flipping the direction on every level.

### Input

The first line contains two integers $n, r$.

Each of the following $n$ lines (line $i$, $1 \le i \le n$) contains two integers $l_i, r_i$: the left and right child of node $i$, where $0$ means no such child.

It is guaranteed that the nodes form a binary tree rooted at $r$: every node has at most one parent, all nodes are reachable from $r$, and there are no cycles.

### Output

One line with $n$ space-separated integers: the node indices in zigzag level order.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le r \le n$
- $0 \le l_i, r_i \le n$
- The depth may be as large as $n$ (a chain), so recursion may overflow the stack

### Sample Explanation

The sample has $n = 7$ and root $1$: node $1$ has children $2, 3$; node $2$ has children $4, 5$; node $3$ has children $6, 7$.

- level $0$: $1$;
- level $1$ left to right is $2, 3$, reversed to $3, 2$;
- level $2$ left to right is $4, 5, 6, 7$, printed as is.

Hence the output is `1 3 2 4 5 6 7`.

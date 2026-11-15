# Count Paths with Obstacles

You are given an $n \times m$ grid $g$, where $g_{i,j} = 1$ marks an obstacle and $g_{i,j} = 0$ marks a free cell.

A robot starts at the top-left cell $(1, 1)$ and may only move **right** or **down** by one cell per step. It wants to reach the bottom-right cell $(n, m)$ without entering an obstacle. Count the number of different paths modulo $10^9+7$.

### Input

The first line contains two integers $n$ and $m$.

The next $n$ lines contain $m$ integers each ($0$ or $1$) describing the grid.

### Output

One integer: the number of paths modulo $10^9+7$. If the target is unreachable, output $0$.

### Constraints

- $1 \le n, m \le 500$
- $g_{i,j} \in \{0, 1\}$

### Sample explanation

The $3 \times 3$ grid has a single obstacle in the centre $(2,2)$. A path from $(1,1)$ to $(3,3)$ uses two moves right and two moves down, so there are $\binom{4}{2} = 6$ paths in total; $2 \times 2 = 4$ of them pass through the centre and are invalid, leaving $6 - 4 = 2$ paths.

### Hint

Let $dp_{i,j}$ be the number of paths reaching $(i,j)$: if $(i,j)$ is an obstacle then $dp_{i,j} = 0$; otherwise $dp_{i,j} = dp_{i-1,j} + dp_{i,j-1}$, with $dp_{1,1} = 1$ (if the start is an obstacle the answer is naturally $0$). Fill the table row by row: one array of length $m$ is enough, because when processing $(i,j)$ the entry $dp_j$ still holds the value from the previous row while $dp_{j-1}$ already holds the current row. The complexity is $O(nm)$.

# Minimum Cost with 0-1 BFS

You are given a grid with $n$ rows and $m$ columns; every cell contains $0$ or $1$. You start at the top-left cell $(1, 1)$ and want to reach the bottom-right cell $(n, m)$.

In one step you may move to one of the four side-adjacent cells (you may not leave the grid). **Entering** a cell $(i, j)$ costs $g_{i,j}$ (either $0$ or $1$); the starting cell $(1,1)$ is free.

Compute the minimum total cost of a walk from $(1,1)$ to $(n,m)$.

### Input

The first line contains two integers $n$ and $m$, separated by a space.

Each of the next $n$ lines contains $m$ integers ($0$ or $1$), separated by spaces: the grid.

### Output

Print one integer: the minimum total cost.

### Constraints

- $1 \le n, m \le 500$
- $g_{i,j} \in \{0, 1\}$
- The cell $(n,m)$ is always reachable from $(1,1)$ (a grid is always connected)
- Time limit 3000 ms, memory limit 256 MB

### Sample

**Input**

```
3 4
0 0 1 1
1 0 1 0
1 1 1 0
```

**Output**

```
1
```

### Sample explanation

The grid is

```
0 0 1 1
1 0 1 0
1 1 1 0
```

Take the route $(1,1) \to (1,2) \to (2,2) \to (2,3) \to (2,4) \to (3,4)$. The cells entered are

$$0,\; 0,\; 1,\; 0,\; 0,$$

so the total cost is $1$. The $2 \times 2$ zero block in the top-left corner is enclosed by $1$s, and the destination lies outside it, so at least one cell of value $1$ must be entered; hence the answer is `1`.

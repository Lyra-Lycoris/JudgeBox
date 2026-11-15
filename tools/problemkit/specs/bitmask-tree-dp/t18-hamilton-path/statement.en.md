# Shortest Hamiltonian Path

There are $n$ cities numbered $0 \sim n-1$. Every ordered pair of cities is connected by a direct flight: flying from city $i$ to city $j$ costs $w_{i,j}$, with $w_{i,i}=0$.

Starting at city $0$ and finishing at city $n-1$, you must visit **every city exactly once** (a Hamiltonian path). Compute the minimum total cost.

### Input

The first line contains one integer $n$.

Each of the next $n$ lines contains $n$ integers; the $j$-th number on the $i$-th line is $w_{i,j}$ (rows and columns are 1-based, so they correspond to cities $i-1$ and $j-1$).

### Output

One integer: the minimum total cost of a path that starts at city $0$, ends at city $n-1$ and visits every city exactly once. For $n=1$ the answer is $0$.

### Constraints

- $1 \le n \le 18$
- $0 \le w_{i,j} \le 10^9$, and $w_{i,i}=0$
- The total cost of any Hamiltonian path is at most $1.7 \times 10^{10}$, so a 64-bit integer is enough
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4
0 3 9 2
3 0 4 8
9 4 0 1
2 8 1 0
```

**Output**

```
8
```

### Sample Explanation

You must start at city $0$, finish at city $3$, and visit cities $1$ and $2$ once each.

- Route $0 \to 1 \to 2 \to 3$ costs $3 + 4 + 1 = 8$;
- Route $0 \to 2 \to 1 \to 3$ costs $9 + 4 + 8 = 21$.

The minimum cost is $8$.

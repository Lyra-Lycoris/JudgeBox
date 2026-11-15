# Shortest TSP Tour

There are $n$ cities numbered $0 \sim n-1$. City $i$ may have a **one-way** flight to city $j$ with cost $w_{i,j}$; $w_{i,j} = -1$ means that flight does not exist. It is guaranteed that $w_{i,i} = 0$.

Starting at city $0$, you must visit **every city exactly once** and then return to city $0$ (a closed tour through all cities). Compute the minimum total cost, or output $-1$ if no such tour exists.

### Input

The first line contains one integer $n$.

Each of the next $n$ lines contains $n$ integers; the $j$-th number on the $i$-th line is $w_{i,j}$ (rows and columns are 1-based, so they correspond to cities $i-1$ and $j-1$).

### Output

One integer: the minimum total cost, or $-1$ if no valid tour exists. For $n=1$ no travel is needed, so the answer is $0$.

### Constraints

- $1 \le n \le 18$
- $w_{i,j} = -1$ (no flight) or $0 \le w_{i,j} \le 10^9$
- $w_{i,i} = 0$
- The answer is at most $1.8 \times 10^{10}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4
0 5 -1 9
7 0 4 -1
-1 6 0 3
2 -1 8 0
```

**Output**

```
14
```

### Sample Explanation

The existing flights are: $0 \to 1$ ($5$), $0 \to 3$ ($9$), $1 \to 0$ ($7$), $1 \to 2$ ($4$), $2 \to 1$ ($6$), $2 \to 3$ ($3$), $3 \to 0$ ($2$), $3 \to 2$ ($8$).

The possible tours:

- $0 \to 1 \to 2 \to 3 \to 0$: $5 + 4 + 3 + 2 = 14$;
- $0 \to 3 \to 2 \to 1 \to 0$: $9 + 8 + 6 + 7 = 30$.

Every other order needs a missing flight (for example $0 \to 2$ or $1 \to 3$), so the minimum total cost is $14$.

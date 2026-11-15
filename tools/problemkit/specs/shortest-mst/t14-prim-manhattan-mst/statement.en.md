# Manhattan MST (Prim)

There are $n$ points in the plane; the $i$-th point has coordinates $(x_i, y_i)$.

Treat the points as vertices and connect every pair $i, j$ with an undirected edge of weight equal to the Manhattan distance

$$d(i, j) = |x_i - x_j| + |y_i - y_j|.$$

This gives a **complete graph** with $\frac{n(n-1)}{2}$ edges. Compute the total weight of its minimum spanning tree.

Coincident points are at distance $0$ from each other.

### Input

The first line contains one integer $n$.

Each of the next $n$ lines contains two integers $x_i$ and $y_i$, separated by a space.

### Output

Print one integer: the total weight of the minimum spanning tree of the complete graph.

### Constraints

- $1 \le n \le 1200$
- $|x_i|, |y_i| \le 10^9$
- Coincident points are allowed
- The answer is at most $4.8 \times 10^{12}$, which fits in a signed 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4
0 0
1 1
3 0
4 5
```

**Output**

```
11
```

### Sample explanation

The pairwise Manhattan distances are $d(1,2)=2$, $d(1,3)=3$, $d(1,4)=9$, $d(2,3)=3$, $d(2,4)=7$, $d(3,4)=6$.

Choosing edges $1-2$ ($2$), $1-3$ ($3$) and $3-4$ ($6$) connects all four points with total weight

$$2 + 3 + 6 = 11.$$

No cheaper connected spanning subgraph exists, so the answer is `11`.

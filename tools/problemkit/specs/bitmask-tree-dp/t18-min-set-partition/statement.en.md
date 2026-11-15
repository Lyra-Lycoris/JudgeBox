# Minimum Cost Set Partition

There are $n$ items numbered $0 \sim n-1$. You must split them into several **non-empty** groups (every item belongs to exactly one group, and the order of groups does not matter).

If one group holds the item set $S$, you pay $c_S$. The set $S$ is encoded as an $n$-bit integer: bit $i$ (for $0 \le i < n$, counted from the least significant bit) is $1$ if item $i$ is in the group. All $2^n$ values $c_S$ are given; find the minimum possible total cost of a complete partition.

### Input

The first line contains one integer $n$.

The second line contains one integer $k$, the size of the cost table, with $k = 2^n$.

The third line contains $k$ integers: $c_0, c_1, \dots, c_{k-1}$. Here $c_0 = 0$ has no meaning, since the empty set is never used.

### Output

One integer: the minimum total cost.

### Constraints

- $1 \le n \le 15$, $k = 2^n$
- $0 \le c_S \le 10^9$, $c_0 = 0$
- The answer is at most $1.5 \times 10^{10}$, so a 64-bit integer is enough
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3
8
0 5 6 4 7 3 9 10
```

**Output**

```
9
```

### Sample Explanation

The cost table for $n=3$ is:

| Set $S$ | binary | meaning | $c_S$ |
|---|---|---|---|
| 1 | 001 | $\{0\}$ | 5 |
| 2 | 010 | $\{1\}$ | 6 |
| 3 | 011 | $\{0,1\}$ | 4 |
| 4 | 100 | $\{2\}$ | 7 |
| 5 | 101 | $\{0,2\}$ | 3 |
| 6 | 110 | $\{1,2\}$ | 9 |
| 7 | 111 | $\{0,1,2\}$ | 10 |

The possible partitions and their costs:

- $\{0,1,2\}$: $10$;
- $\{0\},\{1,2\}$: $5 + 9 = 14$;
- $\{1\},\{0,2\}$: $6 + 3 = 9$;
- $\{2\},\{0,1\}$: $7 + 4 = 11$;
- $\{0\},\{1\},\{2\}$: $5 + 6 + 7 = 18$.

The minimum total cost is $9$.

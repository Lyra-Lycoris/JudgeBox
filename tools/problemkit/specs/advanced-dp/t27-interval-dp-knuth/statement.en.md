# Stone Merging with Knuth Optimization

There are $n$ piles of stones in a row; the $i$-th pile contains $a_i$ stones.

In one operation you may merge **two adjacent piles** into one pile, and the cost of the operation is the total number of stones in the resulting pile. After $n-1$ operations all stones form a single pile.

Find the minimum possible total cost.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

A single line with one integer: the minimum total cost.

### Constraints

- $1 \le n \le 1500$
- $1 \le a_i \le 10^9$
- The minimum total cost is at most $2.3 \times 10^{15}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=4$ and the piles are $1, 2, 3, 4$.

- Merge the first two piles ($1+2$) with cost $3$, giving $3, 3, 4$;
- Merge the first two piles again ($3+3$) with cost $6$, giving $6, 4$;
- Merge the last two piles ($6+4$) with cost $10$.

The total cost is $3 + 6 + 10 = 19$, which is optimal.

### Hint

Let $dp[l][r]$ be the minimum cost of merging the interval $[l, r]$ into one pile, and let $S$ be the prefix sums. Then

$$dp[l][r] = \min_{l \le k < r}\left(dp[l][k] + dp[k+1][r]\right) + S_r - S_{l-1}.$$

A direct implementation is $O(n^3)$, which is too slow for $n = 1500$. Let $opt[l][r]$ be the smallest decision $k$ attaining the minimum. The interval cost (a sum) satisfies the quadrangle inequality, hence the **decision monotonicity**

$$opt[l][r-1] \le opt[l][r] \le opt[l+1][r].$$

Restricting the enumeration of $k$ to $[opt[l][r-1],\, opt[l+1][r]]$ gives the $O(n^2)$ Knuth optimization. Note that $opt[l+1][r]$ may equal $r$, so it must be clamped to $r-1$.

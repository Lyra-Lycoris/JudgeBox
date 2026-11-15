# Weighted Interval Scheduling

You are given $n$ closed intervals; the $i$-th interval is $[l_i, r_i]$ with weight $w_i$.

Choose some of the intervals so that the chosen intervals are **pairwise non-overlapping**, and maximise the total weight (the sum of $w_i$ over the chosen intervals).

Two closed intervals $[l, r]$ and $[l', r']$ are non-overlapping if and only if $r < l'$ or $r' < l$. In other words, intervals that **share an endpoint** (for example $[1, 2]$ and $[2, 3]$) do overlap and cannot both be chosen.

### Input

- The first line contains one integer $n$.
- Each of the next $n$ lines contains three integers $l_i, r_i, w_i$: the endpoints and the weight of the $i$-th interval.

### Output

Print a single integer: the maximum possible total weight of a set of pairwise non-overlapping intervals.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le l_i \le r_i \le 10^{9}$
- $1 \le w_i \le 10^{9}$

The maximum total weight is at most $2 \times 10^{14}$, so it fits into a signed 64-bit integer.

### Sample explanation

Sample 1 has four intervals: $[1,3]$ with weight $5$, $[2,5]$ with weight $6$, $[4,6]$ with weight $5$, $[6,7]$ with weight $4$.

- Taking $[1,3]$ and $[4,6]$: since $3 < 4$, they are non-overlapping, total weight $5 + 5 = 10$.
- Taking $[2,5]$ and $[6,7]$: since $5 < 6$, total weight $6 + 4 = 10$.
- Three intervals are impossible (any two of every three overlap), and the heaviest single interval has weight $6$.

So the maximum total weight is $10$ and the output is `10`.

### Hint

Sort the intervals by **right endpoint** in increasing order (ties broken by the left endpoint), obtaining $[l_1, r_1], \dots, [l_n, r_n]$ with non-decreasing right endpoints.

Let $dp[i]$ be the maximum total weight using only the first $i$ intervals, with $dp[0] = 0$. For the $i$-th interval ($1 \le i \le n$):

- skip it: $dp[i] = dp[i-1]$;
- take it: the intervals placed before it must have right endpoint $< l_i$, so binary search for the last position $k$ whose right endpoint is $< l_i$; the gain is $dp[k] + w_i$.

Thus $dp[i] = \max(dp[i-1], dp[k] + w_i)$ and the answer is $dp[n]$, in $O(n \log n)$ time.

Note that non-overlapping uses a **strict** inequality: an interval whose right endpoint equals $l_i$ shares an endpoint with interval $i$ and cannot be combined with it, so the binary search looks for the first right endpoint that is $\ge l_i$.

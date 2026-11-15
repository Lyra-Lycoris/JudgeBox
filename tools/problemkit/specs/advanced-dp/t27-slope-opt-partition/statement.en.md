# Partition with Convex Segment Cost

Given a sequence of positive integers $a_1, a_2, \dots, a_n$ and a non-negative integer $C$.

You have to split the sequence into several **non-empty contiguous segments**. If a segment covers the index range $[l, r]$, its cost is

$$\left(\sum_{k=l}^{r} a_k\right)^2 + C .$$

Find the minimum possible total cost over all valid splits.

### Input

The first line contains two integers $n$ and $C$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

A single line with one integer: the minimum total cost.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le a_i \le 1000$
- $0 \le C \le 10^6$
- The minimum total cost is at most $4 \times 10^{16}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=3,\ C=10,\ a = (1,2,3)$.

- Split $[1,2,3]$: cost $6^2 + 10 = 46$;
- Split $[1][2,3]$: cost $(1+10) + (25+10) = 46$;
- Split $[1,2][3]$: cost $(9+10) + (9+10) = 38$;
- Split $[1][2][3]$: cost $11 + 14 + 19 = 44$.

The minimum is $38$.

### Hint

Let $S_i = a_1 + \dots + a_i$ be the prefix sums and let $dp[i]$ be the minimum cost of the first $i$ numbers. Then

$$dp[i] = \min_{0 \le j < i}\left(dp[j] + (S_i - S_j)^2 + C\right)
       = S_i^2 + C + \min_{0 \le j < i}\left(dp[j] + S_j^2 - 2 S_i S_j\right).$$

Treat every $j$ as a line with slope $m_j = S_j$ and intercept $b_j = dp[j] + S_j^2$, and query it at $x = -2S_i$. Because $a_i \ge 1$, both $S_j$ and $b_j$ are strictly increasing, while $x$ decreases monotonically with $i$, so a monotone convex hull (slope optimization) evaluates all transitions in $O(n)$.

The hull maintenance compares products such as $\Delta b \cdot \Delta m$, whose value can reach about $10^{25}$, which **does not fit in a 64-bit integer**: use `__int128` in C++, `BigInteger` in Java, a manual 128-bit comparison in Cangjie, and native big integers in Python.

# Number of Ways to Sum to n

Write the positive integer $n$ as a sum of positive integers, each of them at most $m$; **different orders count as different ways**. Output the number of ways modulo $10^9+7$.

For example, with $n = 4, m = 2$ the valid writings are $1+1+1+1$, $1+1+2$, $1+2+1$, $2+1+1$, $2+2$, so there are $5$ ways.

### Input

A single line with two integers $n$ and $m$ separated by a space.

### Output

One integer: the number of ways modulo $10^9+7$.

### Constraints

- $1 \le n \le 10^6$
- $1 \le m \le 10^6$

### Sample explanation

For $n = 4, m = 2$ there are the 5 ways listed above, so the output is $5$.

### Hint

Let $dp[i]$ be the number of ways to write $i$, with $dp[0] = 1$. The last summand can be any of $1 \sim m$, hence

$$dp[i] = \sum_{j=1}^{m} dp[i-j] \quad (i \ge 1)$$

This recurrence costs $O(nm)$ and is too slow. Since $dp[i]$ only depends on the sum of the previous $m$ values, keep a sliding window of $\sum_{j=1}^{m} dp[i-j]$: add $dp[i]$ and remove $dp[i-m]$ each step. That gives $O(n)$. All arithmetic is modulo $10^9+7$.

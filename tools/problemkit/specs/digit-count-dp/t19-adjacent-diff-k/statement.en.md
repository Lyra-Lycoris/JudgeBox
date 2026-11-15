# Adjacent Digits Differ by at Most k

A positive integer is written in decimal without leading zeros. Call it **smooth** if the absolute difference of any two adjacent digits is at most $k$. A one-digit integer is always smooth.

Given $l, r, k$, count the smooth integers in the closed interval $[l, r]$.

### Input

A single line with three integers $l, r, k$ separated by spaces.

### Output

One integer: the number of smooth integers in the interval.

### Constraints

- $1 \le l \le r \le 10^{18}$
- $0 \le k \le 9$

### Sample explanation

For $k = 1$ the smooth integers in $[1, 20]$ are $1 \sim 9$ and $10, 11, 12$, i.e. $9 + 3 = 12$ numbers. $13$ is invalid because $|1-3| = 2 > 1$, and $20$ is invalid because $|2-0| = 2 > 1$.

### Hint

Let $f(x)$ be the number of smooth integers in $[1, x]$; the answer is $f(r) - f(l-1)$. Precompute a small DP table:

$$\text{cnt}[rem][last] = \text{number of ways to append } rem \text{ more digits after } last \text{ while staying smooth}$$

with $\text{cnt}[0][last] = 1$ and $\text{cnt}[rem][last] = \sum_{|v - last| \le k} \text{cnt}[rem-1][v]$.

To compute $f(x)$, first count all smooth numbers shorter than $x$ (their first digit is $1 \sim 9$), then walk along the prefix of $x$: whenever a position can take a smaller digit, add the table value; as soon as the prefix itself violates the condition, stop. One prefix count costs $O(\log_{10} x \cdot 10)$.

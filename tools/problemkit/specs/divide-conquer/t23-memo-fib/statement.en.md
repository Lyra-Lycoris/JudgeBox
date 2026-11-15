# Fibonacci by Memoized Recursion

The Fibonacci sequence is defined as

$$F(0) = 0,\quad F(1) = 1,\quad F(n) = F(n-1) + F(n-2)\ (n \ge 2).$$

Given an integer $n$, compute $F(n) \bmod (10^9 + 7)$.

### Input

One integer $n$.

### Output

A single integer: $F(n) \bmod (10^9 + 7)$.

### Constraints

$0 \le n \le 10^{18}$.

### Sample explanation

Sample 1: $n = 10$ and $F(10) = 55$, so the output is `55`.

Sample 2: $n = 0$ and $F(0) = 0$, so the output is `0`.

Sample 3: $n = 1$ and $F(1) = 1$, so the output is `1`.

### Hint

Recursing directly on the definition recomputes the same subproblems exponentially many times; with memoization (storing already computed $F(k)$) each subproblem is solved once and the complexity drops to $O(n)$. However, here $n$ can be as large as $10^{18}$, so $O(n)$ is still too slow.

The following identities halve the problem size:

$$F(2k) = F(k)\bigl(2F(k+1) - F(k)\bigr),$$
$$F(2k+1) = F(k)^2 + F(k+1)^2.$$

Recursively obtain $(F(k), F(k+1))$ for $k = \lfloor n/2 \rfloor$, then combine them into $(F(n), F(n+1))$; the recursion depth is only $O(\log n)$. All arithmetic is done modulo $10^9 + 7$; note that $2F(k+1) - F(k)$ may be negative, so add the modulus before reducing.

# Number of Ways to Choose k of n Items

How many ways are there to choose $k$ out of $n$ distinct items? The answer can be large, so print it modulo $10^9+7$.

Formally, compute the binomial coefficient

$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!} \bmod (10^9+7).$$

The chosen $k$ items are unordered: from $\{1,2,3\}$ one can choose $2$ items in the three ways $\{1,2\}, \{1,3\}, \{2,3\}$ only.

### Input

A single line with two integers $n$ and $k$ separated by a single space.

### Output

One line with a single integer: the value of $\binom{n}{k} \bmod (10^9+7)$, lying in $[0, 10^9+6]$.

### Constraints

- $0 \le k \le n \le 200000$
- The modulus $10^9+7$ is prime, so $k!$ and $(n-k)!$ are invertible modulo $10^9+7$

### Sample explanation

Sample 1: $n = 5$, $k = 2$, and $\binom{5}{2} = \dfrac{5 \times 4}{2 \times 1} = 10$, which stays $10$ modulo $10^9+7$.

Sample 2: $n = 0$, $k = 0$; the empty set has exactly one subset of size $0$, so the answer is $1$.

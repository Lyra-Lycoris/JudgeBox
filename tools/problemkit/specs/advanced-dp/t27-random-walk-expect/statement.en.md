# Expected Steps of a Random Walk

The number line has positions $0, 1, 2, \dots$. You start at position $0$.

At every step you move $1$ position forward with probability $p = \dfrac{P}{P+Q}$ and $2$ positions forward with probability $q = \dfrac{Q}{P+Q}$, where $P, Q$ are non-negative integers with $P + Q > 0$.

You stop as soon as your position is **at least** $n$. Find the expected number of steps until you stop.

The expectation may be a rational number. Write it as a reduced fraction $\dfrac{A}{B}$ ($B > 0$, $\gcd(A,B)=1$) and output

$$A \cdot B^{-1} \bmod (10^9+7),$$

where $B^{-1}$ is the multiplicative inverse of $B$ modulo $10^9+7$. For the given constraints $B$ is never a multiple of $10^9+7$.

### Input

A single line with three integers $n, P, Q$.

### Output

A single line with one integer: the expected number of steps modulo $10^9+7$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $0 \le P, Q \le 10^9$
- $1 \le P + Q \le 10^9$
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=5,\ P=Q=1$, hence $p=q=\frac12$.

Let $E_i$ be the expected number of remaining steps from position $i$. Then $E_i = 0$ for $i \ge 5$ and $E_i = 1 + \frac12 E_{i+1} + \frac12 E_{i+2}$ for $i < 5$. Computing backwards:

- $E_4 = 1$;
- $E_3 = 1 + \frac12 E_4 = \frac32$;
- $E_2 = 1 + \frac12 E_3 + \frac12 E_4 = \frac94$;
- $E_1 = 1 + \frac12 E_2 + \frac12 E_3 = \frac{23}{8}$;
- $E_0 = 1 + \frac12 E_1 + \frac12 E_2 = \frac{57}{16}$.

Thus the answer is $57 \cdot 16^{-1} \bmod (10^9+7) = 62500004$.

### Hint

Let $E_i$ be the expected number of steps from position $i$. Since the walk stops once the position is $\ge n$, we have $E_i = 0$ for $i \ge n$, and for $0 \le i < n$

$$E_i = 1 + p\,E_{i+1} + q\,E_{i+2}.$$

Computing $i$ from $n-1$ down to $0$ takes $O(n)$ time. Everything is done modulo $10^9+7$: $p = P \cdot (P+Q)^{-1}$ and $q = Q \cdot (P+Q)^{-1}$, with the inverse obtained by fast exponentiation.

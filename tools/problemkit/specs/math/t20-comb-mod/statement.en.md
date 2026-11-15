# Binomial Coefficient Modulo a Prime

Given integers $n, k$ and a prime $p$, compute

$$\binom{n}{k} \bmod p ,$$

where $0 \le k \le n \le 10^6$ and $n < p$.

**Approach**: since $n < p$, none of $1, 2, \dots, n$ is a multiple of $p$, so in

$$\binom{n}{k} = \frac{n (n-1) \cdots (n-k+1)}{k!}$$

both the numerator and the denominator are non-zero modulo $p$. Multiply the numerator and the denominator separately, then obtain the inverse of the denominator with Fermat's little theorem:

$$x^{-1} \equiv x^{p-2} \pmod p .$$

Hence $\binom{n}{k} \equiv \text{numerator} \times \text{denominator}^{p-2} \pmod p$, in $O(k \log p)$ time. Replacing $k$ by $\min(k, n-k)$ first halves the work.

### Input

A single line with three integers $n, k, p$ separated by single spaces.

### Output

One line with a single integer: the value of $\binom{n}{k} \bmod p$, lying in $[0, p-1]$.

### Constraints

$0 \le k \le n \le 10^6$, $p$ is prime and $n < p \le 10^9+7$.

### Sample explanation

$\binom{5}{2} = \dfrac{5 \times 4}{2 \times 1} = 10$, and $10 \bmod (10^9+7) = 10$, so the output is `10`.

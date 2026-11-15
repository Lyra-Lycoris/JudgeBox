# Recursive Fast Exponentiation

Given three integers $a, b, m$, compute $a^b \bmod m$. We define $0^0 = 1$, so when $a = b = 0$ the answer is $1 \bmod m$.

### Input

One line with three integers $a, b, m$ separated by single spaces.

### Output

A single integer: $a^b \bmod m$.

### Constraints

- $0 \le a \le 10^9$
- $0 \le b \le 10^{18}$
- $1 \le m \le 2 \times 10^9$

### Sample explanation

Sample 1: $a = 2$, $b = 10$, $m = 1000$. $2^{10} = 1024$ and $1024 \bmod 1000 = 24$, so the output is `24`.

Sample 2: $a = 0$, $b = 0$, $m = 7$. By definition $0^0 = 1$ and $1 \bmod 7 = 1$, so the output is `1`.

Sample 3: $a = 123456789$, $b = 10^{18}$, $m = 10^9 + 7$, and the output is `228100152`.

### Hint

Halve the exponent: if $b$ is even then $a^b = (a^{b/2})^2$, otherwise $a^b = (a^{b/2})^2 \cdot a$. The recursion has depth $O(\log b)$, and reducing modulo $m$ after every multiplication avoids overflow. The total complexity is $O(\log b)$.

Note that $a$ and $m$ are not necessarily coprime, so Fermat's little theorem and the extended Euler theorem do not apply; the plain halving recursion is enough.

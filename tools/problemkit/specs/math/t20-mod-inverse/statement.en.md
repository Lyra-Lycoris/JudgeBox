# Modular Inverse via Extended Euclid

Given two positive integers $a$ and $m$ with $m \ge 2$, find the multiplicative inverse of $a$ modulo $m$: the smallest non-negative integer $x$ such that

$$a x \equiv 1 \pmod m .$$

If no such $x$ exists, print $-1$.

**Existence**: $a$ has an inverse modulo $m$ if and only if $\gcd(a, m) = 1$.

**How to compute it**: the extended Euclidean algorithm produces integers $(x, y)$ with $a x + m y = \gcd(a, m) = 1$; then $x \bmod m$ is the answer. One query costs $O(\log m)$.

### Input

A single line with two integers $a, m$ separated by a single space.

### Output

One line with a single integer: the smallest non-negative inverse of $a$ modulo $m$, or `-1` if the inverse does not exist.

### Constraints

$1 \le a \le 10^9$, $2 \le m \le 10^9$.

### Sample explanation

For $a = 3$ and $m = 11$: $3 \times 4 = 12 = 11 + 1 \equiv 1 \pmod{11}$, so the inverse is $4$. Note that $\gcd(3, 11) = 1$, so the inverse is guaranteed to exist.

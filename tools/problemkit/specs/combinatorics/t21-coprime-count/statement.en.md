# Numbers Coprime to m

Given two positive integers $n$ and $m$, count the integers $x$ with $1 \le x \le n$ and $\gcd(x, m) = 1$.

For $n = 10$ and $m = 6$ the numbers coprime to $6$ are $1, 5, 7$, so the answer is $3$.

### Input

A single line with two integers $n$ and $m$ separated by a single space.

### Output

One integer: the number of valid $x$.

### Constraints

- $1 \le n \le 10^{18}$
- $1 \le m \le 10^{12}$
- For $m = 1$ every number is coprime to $m$, so the answer is $n$

### Sample explanation

Sample 1: $n = 10$, $m = 6 = 2 \times 3$. Among $1, 2, \dots, 10$ there are $5$ multiples of $2$, $3$ multiples of $3$ and $1$ multiple of $6$. By inclusion-exclusion, $5 + 3 - 1 = 7$ numbers are not coprime to $6$, so $10 - 7 = 3$ numbers are, namely $1, 5, 7$.

Sample 2: $n = 100$, $m = 12 = 2^2 \times 3$; only the prime factors $2$ and $3$ matter. Every block of $12$ consecutive integers contains $\varphi(12) = 4$ numbers coprime to $12$. Since $100 = 8 \times 12 + 4$, the first $96$ numbers contribute $32$, and among $97, 98, 99, 100$ only $97$ is coprime to $12$, so the answer is $33$.

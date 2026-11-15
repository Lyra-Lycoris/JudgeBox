# Climbing Stairs

A staircase has $n$ steps. You start on the ground (step $0$) and on every move you climb either $1$ or $2$ steps. You must finish exactly on step $n$.

Count the number of different ways to reach step $n$. Two ways are different if at some move the number of climbed steps differs.

The answer may be huge, so output the number of ways modulo $10^9+7$.

### Input

A single integer $n$.

### Output

A single integer: the number of ways modulo $10^9+7$.

### Constraints

$1 \le n \le 500000$.

### Sample explanation

Sample 1: $n = 5$. There are $8$ valid ways:

- $1+1+1+1+1$
- $1+1+1+2$
- $1+1+2+1$
- $1+2+1+1$
- $2+1+1+1$
- $1+2+2$
- $2+1+2$
- $2+2+1$

So the output is `8`.

### Hint

Let $f_i$ be the number of ways to reach step $i$. Then $f_0 = 1$, $f_1 = 1$, and for $i \ge 2$, $f_i = f_{i-1} + f_{i-2}$. The answer is $f_n \bmod (10^9+7)$.

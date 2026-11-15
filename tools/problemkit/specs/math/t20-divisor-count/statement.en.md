# Number of Divisors

Given a positive integer $n$, count how many positive divisors $n$ has.

For example, the positive divisors of $12$ are $1, 2, 3, 4, 6, 12$, so there are $6$ of them.

Since $n$ can be as large as $10^{12}$, scanning every integer from $1$ to $n$ is too slow. Divisors come in pairs: if $d$ divides $n$, then so does $n/d$. Hence it suffices to scan $1 \le d \le \lfloor\sqrt{n}\rfloor$; every such divisor contributes two divisors, except when $d = n/d$ (that is, $n$ is a perfect square), where it contributes only one. The complexity is $O(\sqrt{n})$.

### Input

A single line with one integer $n$.

### Output

One line with a single integer: the number of positive divisors of $n$.

### Constraints

$1 \le n \le 10^{12}$.

### Sample explanation

For $n = 12$, scanning $d = 1, 2, 3$ finds three divisors, and none of $1^2, 2^2, 3^2$ equals $12$, so each contributes two divisors: $2 \times 3 = 6$.

# Linear Recurrence by Matrix Exponentiation

Define the sequence $f$ by

$$f(0) = x,\qquad f(1) = y,\qquad f(i) = p \cdot f(i-1) + q \cdot f(i-2)\quad (i \ge 2).$$

Given $n, x, y, p, q$, compute $f(n) \bmod (10^9+7)$.

Since $n$ can be as large as $10^{18}$, iterating the recurrence is impossible. Rewrite it in matrix form:

$$\begin{pmatrix} f(i) \\ f(i-1) \end{pmatrix}
= \begin{pmatrix} p & q \\ 1 & 0 \end{pmatrix}
  \begin{pmatrix} f(i-1) \\ f(i-2) \end{pmatrix},$$

so binary exponentiation of a $2 \times 2$ matrix solves the problem in $O(\log n)$ matrix multiplications.

### Input

A single line with five integers $n, x, y, p, q$.

### Output

A single line with one integer: $f(n) \bmod (10^9+7)$.

### Constraints

- $0 \le n \le 10^{18}$
- $0 \le x, y, p, q \le 10^9+6$
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: with $x=1,\ y=1,\ p=1,\ q=1$ the sequence is $1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, \dots$, hence $f(10)=89$.

If $n=0$ the answer is $x$; if $n=1$ the answer is $y$. These two boundaries need no matrix multiplication.

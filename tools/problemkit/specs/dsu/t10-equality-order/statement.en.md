# Equality and Order Constraints

There are $n$ integer variables $x_1, x_2, \dots, x_n$. Each variable may take any integer value (negatives are allowed and there is no bound).

You are given $k$ constraints, each of one of the following two forms:

- $x_u = x_v$ (with $t = 0$ in the input);
- $x_u < x_v$ (with $t = 1$ in the input).

Determine whether there is an integer assignment satisfying all $k$ constraints simultaneously.

### Input

- The first line contains two integers $n$ and $k$, separated by a single space.
- Each of the next $k$ lines contains three integers $t, u, v$ as described above. $t = 0$ means $x_u = x_v$, and $t = 1$ means $x_u < x_v$.

### Output

Print `YES` on a single line if a satisfying assignment exists, otherwise print `NO`.

### Constraints

$1 \le n \le 200000$, $0 \le k \le 200000$, $t \in \{0, 1\}$, $1 \le u, v \le n$.

It is allowed that $u = v$; then a constraint with $t = 1$ requires $x_u < x_u$ and is impossible. The same constraint may be given more than once.

### Sample explanation

Sample 1: $n = 4$ with constraints $x_1 = x_2$, $x_2 < x_3$, $x_3 = x_4$ and $x_1 < x_4$.

First merge the equal variables: $\{x_1, x_2\}$ share one value $a$ and $\{x_3, x_4\}$ share one value $b$. The constraints become $a < b$ and $a < b$, which agree. Taking $a = 0$ and $b = 1$ satisfies everything, so the answer is `YES`.

If the second constraint were $x_3 < x_2$ instead, the requirements would become $a < b$ and $b < a$, a contradiction, and the answer would be `NO`.

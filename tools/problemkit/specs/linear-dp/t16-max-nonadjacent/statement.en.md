# Maximum Sum of Non-Adjacent Elements

A street has $n$ houses in a row. House $i$ contains $a_i$ coins, where $a_i$ is a non-negative integer.

You want to collect as much money as possible, but you may **not** take the money from two adjacent houses (that would trigger the alarm).

Compute the maximum amount of money you can collect. Taking nothing is allowed, and then the answer is $0$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the maximum amount of money you can collect.

### Constraints

$1 \le n \le 200000$, $0 \le a_i \le 10^9$.

The answer is at most $10^{14}$, so a 64-bit integer is enough.

### Sample explanation

Sample 1: $n = 5$ and the amounts are $2, 7, 9, 3, 1$.

Taking houses $1, 3, 5$ gives $2 + 9 + 1 = 12$; taking houses $2, 4$ gives $7 + 3 = 10$. The maximum is $12$, so the output is `12`.

### Hint

Run a linear DP from left to right. Let

- $f_i$: the best amount using the first $i$ houses while **not** taking house $i$;
- $g_i$: the best amount using the first $i$ houses while **taking** house $i$.

Then $g_i = f_{i-1} + a_i$ and $f_i = \max(f_{i-1}, g_{i-1})$, and the answer is $\max(f_n, g_n)$. Only two values need to be stored, so the extra space is $O(1)$.

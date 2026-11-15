# Minimum Operations to Reach the Target Array

You are given two integer arrays of length $n$: $a_1, \dots, a_n$ and $b_1, \dots, b_n$.

In one operation you may pick any **contiguous subarray** $[l, r]$ ($1 \le l \le r \le n$) and then either

- add $1$ to $a_l, a_{l+1}, \dots, a_r$; or
- subtract $1$ from $a_l, a_{l+1}, \dots, a_r$.

Find the minimum number of operations needed to turn $a$ into $b$ (so that $a_i = b_i$ for every $i$).

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, \dots, a_n$.
- The third line contains $n$ integers $b_1, \dots, b_n$.

### Output

A single integer: the minimum number of operations.

### Constraints

$1 \le n \le 200000$, $-10^9 \le a_i, b_i \le 10^9$.

### Sample explanation

Sample 1: $n = 3$, $a = (1, 2, 3)$, $b = (3, 2, 1)$. The differences $d_i = b_i - a_i$ are $(2, 0, -2)$: position $1$ must be increased twice and position $3$ decreased twice. Since position $2$ must stay unchanged, the two positions can never share an operation, so at least $4$ operations are needed, and $4$ suffice (for example add $1$ twice to $[1,1]$ and subtract $1$ twice from $[3,3]$).

### Hint

Let $d_i = b_i - a_i$ and split it into a positive and a negative part: $p_i = \max(d_i, 0)$ and $q_i = \max(-d_i, 0)$.

- The positive part can only be handled by "add $1$" operations and the negative part only by "subtract $1$" operations, so the two are independent.
- For the positive part, one "add $1$" operation covers one layer of a contiguous range. With $p_0 = 0$, the number of "add $1$" operations is exactly $\sum_i \max(0, p_i - p_{i-1})$ (a new operation must start whenever the needed height grows, and it can end whenever the height drops).
- Symmetrically, the number of "subtract $1$" operations is $\sum_i \max(0, q_i - q_{i-1})$ with $q_0 = 0$.

The answer is the sum of both parts, computed in $O(n)$. Note that the answer can be large (up to about $2 \times 10^{14}$), so 64-bit integers are required.

# Maximum Subarray Sum

Given a sequence of $n$ integers $a_1, a_2, \dots, a_n$ (elements may be positive, negative or zero), find a **non-empty** contiguous subarray $a_l, a_{l+1}, \dots, a_r$ ($1 \le l \le r \le n$) whose sum is as large as possible, and output that maximum sum.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the maximum sum of a non-empty contiguous subarray.

### Constraints

$1 \le n \le 200000$, $-10^9 \le a_i \le 10^9$.

The absolute value of the answer is at most $2 \times 10^{14}$, so a 64-bit integer is enough.

### Sample explanation

Sample 1: $n = 9$ and the sequence is $-2, 1, -3, 4, -1, 2, 1, -5, 4$.

Take the subarray $a_4 \dots a_7$, namely $4, -1, 2, 1$, whose sum is $4 - 1 + 2 + 1 = 6$. No other non-empty contiguous subarray has a larger sum, so the output is `6`.

### Hint

Let $f_i$ be the best sum of a subarray ending at position $i$. Then $f_1 = a_1$ and $f_i = \max(a_i, f_{i-1} + a_i)$; the answer is the maximum of all $f_i$. This runs in $O(n)$.

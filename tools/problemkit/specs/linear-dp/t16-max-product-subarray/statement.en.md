# Maximum Product Subarray

Given an integer array $a$ of length $n$, where every element $a_i$ is one of $-2, -1, 0, 1, 2$.

Find a **non-empty** contiguous subarray $a_l, a_{l+1}, \dots, a_r$ ($1 \le l \le r \le n$) whose product is as large as possible, and output that maximum product.

The answer may be negative: if the array is just a single $-2$, the answer is $-2$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the maximum product of a contiguous subarray.

### Constraints

$1 \le n \le 200000$, $a_i \in \{-2, -1, 0, 1, 2\}$.

The data guarantees that the **absolute value of the product of every contiguous subarray** is at most $10^{18}$, so the answer fits in a 64-bit integer.

### Sample explanation

Sample 1: $n = 5$ and the array is $2, -2, -1, 0, 1$.

- The subarray $a_1 \dots a_3$ has product $2 \times (-2) \times (-1) = 4$.
- All other subarrays have products $2, -4, -2, -1, 0, 0, 0, 1$, and so on, none larger than $4$.

Hence the maximum product is $4$ and the output is `4`.

### Hint

Keeping only the maximum product ending at the current position is not enough, because multiplying by a negative number turns a maximum into a minimum. Track both:

- $mx_i$: the maximum product of a subarray ending at $i$;
- $mn_i$: the minimum product of a subarray ending at $i$.

Then $mx_i = \max(a_i,\ mx_{i-1} \cdot a_i,\ mn_{i-1} \cdot a_i)$ and $mn_i = \min(a_i,\ mx_{i-1} \cdot a_i,\ mn_{i-1} \cdot a_i)$, and the answer is the maximum of all $mx_i$. The complexity is $O(n)$.

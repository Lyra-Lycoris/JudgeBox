# Maximum Subarray Sum by Divide and Conquer

Given a sequence of $n$ integers $a_1, a_2, \dots, a_n$ (elements may be positive, negative or zero), find a **non-empty** contiguous subarray $a_l, a_{l+1}, \dots, a_r$ ($1 \le l \le r \le n$) whose sum is as large as possible, and output that maximum sum.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the maximum sum of a non-empty contiguous subarray.

### Constraints

$1 \le n \le 200000$, $-10^9 \le a_i \le 10^9$.

The absolute value of the answer is at most $2 \times 10^{14}$, so a 64-bit integer is required.

### Sample explanation

Sample 1: $n = 9$ and the sequence is $-2, 1, -3, 4, -1, 2, 1, -5, 4$. Taking $a_4 \dots a_7$, namely $4, -1, 2, 1$, gives $4 - 1 + 2 + 1 = 6$, which is the largest possible sum, so the output is `6`.

Sample 2: $n = 5$ and all values are negative, so the best subarray is a single element $-1$; the output is `-1`.

Sample 3: $n = 1$, the only subarray is the whole sequence, so the output is `-1000000000`.

### Hint

Use divide and conquer. Split the sequence at $mid$ into a left half and a right half; the best subarray is one of three kinds:

1. completely inside the left half $[1, mid]$;
2. completely inside the right half $[mid+1, n]$;
3. crossing the middle, i.e. $[l, r]$ with $l \le mid < r$. Its sum equals the best suffix of the left half ending at $mid$ plus the best prefix of the right half starting at $mid+1$; both are found by scanning outwards from the middle in $O(n)$.

Thus $T(n) = 2T(n/2) + O(n)$ and the total complexity is $O(n \log n)$. An $O(n)$ dynamic programming solution is also accepted.

# Maximum Subarray Sum of a Range (Segment Tree)

You are given an integer array $a_1, a_2, \dots, a_n$ of length $n$ and $q$ queries. Each query gives $l, r$ and asks for

$$\max_{l \le i \le j \le r} \sum_{k=i}^{j} a_k,$$

the largest sum of a **non-empty** contiguous subarray inside $[l, r]$. The subarray must be non-empty, so the answer is at least the maximum element of the range.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains two integers $l, r$, describing one query.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 2 \times 10^4$
- $1 \le l \le r \le n$
- $|a_i| \le 10^9$

### Sample explanation

The array is $2, -3, 4, -1, 2, -5, 3$.

`1 7` asks for the whole array: taking the subarray $[3, 5]$ gives $4 + (-1) + 2 = 5$, while the sum of everything is only $2$, so the answer is $5$.

`3 5` asks for $[3, 5]$, which can only be taken as a whole: $4 + (-1) + 2 = 5$.

`1 2` asks for $[1, 2]$, i.e. the values $2, -3$; taking $[1, 1]$ gives $2$.

`2 6` asks for $[-3, 4, -1, 2, -5]$; taking the subarray $[2, 5]$ gives $4 + (-1) + 2 = 5$.

`4 4` asks for a single position, so the answer is $a_4 = -1$.

Hence the output is `5 5 2 5 -1`.

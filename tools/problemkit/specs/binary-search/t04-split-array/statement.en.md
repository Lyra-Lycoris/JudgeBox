# Split Array Largest Sum

You are given an array $a_0, a_1, \dots, a_{n-1}$ of $n$ non-negative integers and an integer $k$.

Split the array into $k$ **non-empty** contiguous subarrays (by choosing $k-1$ cut positions) so that the largest subarray sum among the $k$ parts is as small as possible.

Return that minimal possible largest subarray sum.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_0, a_1, \dots, a_{n-1}$.

The third line contains one integer $k$.

### Output

One integer: the minimal possible largest subarray sum.

### Constraints

- $1 \le k \le n \le 2 \times 10^5$
- $0 \le a_i \le 10^9$
- $\sum a_i \le 2 \times 10^{14}$ is guaranteed, so the answer fits in a 64-bit integer

### Sample explanation

With $n = 5$, the array $7, 2, 5, 10, 8$ and $k = 2$, the possible splits are:

- $[7] \mid [2, 5, 10, 8]$: sums $7$ and $25$, maximum $25$.
- $[7, 2] \mid [5, 10, 8]$: $9$ and $23$, maximum $23$.
- $[7, 2, 5] \mid [10, 8]$: $14$ and $18$, maximum $18$.
- $[7, 2, 5, 10] \mid [8]$: $24$ and $8$, maximum $24$.

The minimal possible maximum is $18$, so the answer is $18$.

To test whether "every part sums to at most $S$" is feasible, greedily fill each part from left to right and count how many parts are needed. Since all values are non-negative, the needed number of parts never increases as $S$ grows, so the answer can be binary searched in $[\max a_i, \sum a_i]$.

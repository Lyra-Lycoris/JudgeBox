# Count Subarrays with Sum K

Given $n$ integers $a_1, a_2, \dots, a_n$ and an integer $k$, count how many **contiguous subarrays** (that is, segments $a_l, a_{l+1}, \dots, a_r$ with $1 \le l \le r \le n$) have a sum exactly equal to $k$.

The subarray must be non-empty, and different index ranges count as different subarrays.

### Input

- The first line contains two integers $n$ and $k$, separated by a space.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

Print one integer: the number of contiguous subarrays whose sum equals $k$.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$, $|k| \le 10^{14}$.

### Sample explanation

In sample 1, $n = 5$, $k = 3$ and the sequence is $1, 1, 1, 1, 1$. Exactly three contiguous subarrays have sum $3$:

- $a_1 + a_2 + a_3$;
- $a_2 + a_3 + a_4$;
- $a_3 + a_4 + a_5$.

So the answer is `3`.

Note that $a_i$ may be negative or zero, so prefix sums can repeat and the answer can be large; it has to be stored in a 64-bit integer.

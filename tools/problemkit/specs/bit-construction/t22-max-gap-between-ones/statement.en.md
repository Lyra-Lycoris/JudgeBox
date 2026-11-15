# Maximum Gap Between Adjacent Ones

Given a non-negative integer $n$, consider its binary representation (without leading zeros). Let the positions of its $1$ bits, from the least significant one upwards, be

$$p_1 < p_2 < \dots < p_k$$

(where the least significant bit is position $0$). The **maximum gap** of $n$ is defined as:

- if $k < 2$, the maximum gap is $0$;
- otherwise, the maximum gap is $\max_{1 \le i < k} \left(p_{i+1} - p_i - 1\right)$, i.e. the largest number of zeros squeezed between two adjacent $1$ bits.

Note that the zeros below the lowest $1$ and above the highest $1$ are not "between two adjacent ones" and do not count.

You are given $T$ non-negative integers; compute the maximum gap of each of them.

### Input

- The first line contains one integer $T$.
- The following $T$ lines each contain one integer $n$.

### Output

Print $T$ lines, each containing the maximum gap of the corresponding integer.

### Constraints

- $1 \le T \le 200000$;
- $0 \le n \le 10^{18}$.

Since $10^{18} < 2^{60}$, every number has at most $60$ bits (indices $0 \sim 59$), so the answer is at most $58$: with $n = 2^{59}+1$ the two $1$ bits sit at positions $0$ and $59$.

### Sample explanation

The sample has $T = 3$ with the numbers $9, 5, 100$.

- $n = 9 = (1001)_2$: the $1$ bits are at positions $0$ and $3$, with $3 - 0 - 1 = 2$ zeros in between, so the maximum gap is $2$.
- $n = 5 = (101)_2$: the $1$ bits are at positions $0$ and $2$, with one zero in between, so the maximum gap is $1$.
- $n = 100 = (1100100)_2$: the $1$ bits are at positions $2, 5, 6$. The adjacent gaps are $5-2-1 = 2$ and $6-5-1 = 0$, so the maximum gap is $2$.

The output is therefore `2`, `1`, `2`.

### Hint

Scan from the least significant bit upwards. Keep `last`, the position of the previous $1$ bit (initially "none"), and `pos`, the index of the bit being processed.

- If `n & 1` is $1$: when `last` exists, update the answer with `pos - last - 1`, then set `last = pos`;
- regardless of the bit value, do `n >>= 1` and `pos += 1`.

This takes about $60$ iterations per number, so $O(60T)$ in total. A natural alternative is to write a helper that solves a single number and call it $T$ times.

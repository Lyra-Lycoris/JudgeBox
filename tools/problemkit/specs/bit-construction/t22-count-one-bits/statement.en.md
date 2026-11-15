# Number of 1 Bits

Given a non-negative integer $n$, count how many digits equal to $1$ appear in the binary representation of $n$ (without leading zeros). This quantity is also called the **popcount** of $n$.

For example, $n = 11$ is $(1011)_2$ in binary and contains $3$ ones, so the answer is $3$.

### Input

A single line with one integer $n$.

### Output

A single line with one integer: the number of $1$ bits in the binary representation of $n$.

### Constraints

- $0 \le n \le 2^{63}-1$, that is $0 \le n \le 9223372036854775807$.

For $n = 0$ the binary representation is considered to be `0`, so the answer is $0$. The binary representation has at most $63$ bits, hence the answer is at most $63$ and fits into a 64-bit integer.

### Sample explanation

**Sample 1**: $n = 11 = (1011)_2$. Reading the four bits from the least significant one gives $1, 1, 0, 1$, so there are $3$ ones and the output is `3`.

**Sample 2**: $n = 9223372036854775807 = 2^{63}-1 = (111\cdots111)_2$, namely $63$ consecutive ones, so the output is `63`.

### Hint

Let `lowbit(x) = x & (-x)`, which extracts the lowest set bit of $x$. Repeating

```
x = x & (x - 1)
```

removes exactly one set bit per iteration, so the number of iterations equals the number of ones. The complexity is $O(\text{popcount}(n))$, that is $O(\log n)$ in the worst case.

Another option is to loop over bits $0 \sim 62$ and test whether `(n >> i) & 1` is $1$.

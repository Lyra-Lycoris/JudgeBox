# Construct a Permutation with k Prefix Maxima

You are given two integers $n$ and $k$.

Construct a permutation $p_1, p_2, \dots, p_n$ of $1, 2, \dots, n$ (every integer from $1$ to $n$ appears exactly once) such that it has **exactly $k$ prefix maxima**.

A position $i$ is a prefix maximum if and only if $p_i$ is strictly greater than every element before it, i.e. $p_i > \max(p_1, \dots, p_{i-1})$ (with $p_0 = 0$). Hence the first position is always a prefix maximum.

This problem uses a **special judge** (SPJ): any valid permutation is accepted; it does not have to match the reference output.

### Input

A single line with two integers $n$ and $k$, separated by one space.

### Output

Print $n$ integers: your permutation. The numbers may be separated by spaces or newlines, but their relative order must be kept. You must print exactly $n$ numbers.

### Constraints

$1 \le k \le n \le 200000$.

### Sample explanation

Sample 1: $n = 5$, $k = 3$. The output `1 2 5 4 3` is valid: the prefix maxima are at positions $1, 2, 3$ (values $1, 2, 5$), while $4$ and $3$ are both smaller than $5$, so there are exactly $3$ prefix maxima.

For instance `1 5 2 3 4` has only $2$ prefix maxima, `5 4 3 2 1` has $1$ and `1 2 3 4 5` has $5$, so a construction is really needed for $k = 3$.

### Hint

First place $1, 2, \dots, k-1$ in increasing order, which gives $k-1$ prefix maxima. Then append $n, n-1, \dots, k$. Only the leading $n$ becomes a new prefix maximum, because every following value is smaller than $n$. The total is exactly $k$.

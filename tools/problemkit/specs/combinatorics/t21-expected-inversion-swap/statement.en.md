# Expected Inversions After a Random Swap

Given an integer array $a_1, a_2, \dots, a_n$ of length $n$. A pair of indices $(i, j)$ is an **inversion** if $i < j$ and $a_i > a_j$.

Pick one of the $\binom{n}{2}$ index pairs $i < j$ uniformly at random, swap $a_i$ and $a_j$, and obtain a **new array**. Compute the expected number of inversions in the new array.

The expectation may be a fraction, so this problem expects it modulo $10^9+7$:

> If the answer is the reduced fraction $p/q$ (with $q$ coprime to $10^9+7$), print
> $$p \cdot q^{-1} \bmod (10^9+7),$$
> where $q^{-1}$ is the modular inverse of $q$ modulo $10^9+7$.

Note: if the swap does not change the array (for instance the two positions hold equal values), it still counts as a valid swap and the number of inversions stays the same.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by spaces.

### Output

One integer: the expected value modulo $10^9+7$, lying in $[0, 10^9+6]$.

### Constraints

- $1 \le n \le 200000$
- $|a_i| \le 10^9$
- For $n = 1$ there is no index pair, and the answer is defined as $0$

### Sample explanation

Sample 1: $n = 3$ with the array $3, 1, 2$. There are $\binom{3}{2} = 3$ index pairs:

- swapping $(1, 2)$ gives $1, 3, 2$ with $1$ inversion;
- swapping $(1, 3)$ gives $2, 1, 3$ with $1$ inversion;
- swapping $(2, 3)$ gives $3, 2, 1$ with $3$ inversions.

All three swaps are equally likely, so the expectation is $(1 + 1 + 3)/3 = 5/3$. Since $3^{-1} \equiv 333333336$, we get $5 \times 333333336 \bmod (10^9+7) = 666666673$, so the output is `666666673`.

Sample 2: $n = 1$; no index pair exists, so the answer is defined as $0$.

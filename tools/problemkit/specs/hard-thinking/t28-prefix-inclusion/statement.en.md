# Inclusion-Exclusion: Numbers Matching at Least One Condition

You are given a positive integer $n$ and $m$ conditions. Each condition is one of the following two kinds:

- **Divisibility condition** `1 k`: the integer $x$ is a multiple of $k$. The input guarantees that $k$ is a power of two, i.e. $k = 2^{p}$ with $0 \le p \le 20$, so this condition is equivalent to "the lowest $p$ bits of $x$ are all $0$";
- **Bit condition** `2 b`: bit $b$ of the binary representation of $x$ is $1$ ($0 \le b \le 59$, the least significant bit is bit $0$).

Count how many integers $x \in [1, n]$ satisfy **at least one** of the $m$ conditions.

### Input

- The first line contains two integers $n$ and $m$.
- Each of the next $m$ lines contains two integers $t, x$ describing one condition:
  - if $t = 1$, $x$ is the value $k$ and the condition is "$x$ is a multiple of $k$"; here $x$ is always a power of two;
  - if $t = 2$, $x$ is the index $b$ and the condition is "bit $b$ of $x$ is $1$".

### Output

Print a single integer: the number of integers in $[1, n]$ that satisfy at least one condition.

### Constraints

- $1 \le n \le 10^{18}$
- $1 \le m \le 8$
- $t \in \{1, 2\}$
- for $t = 1$: $k = x$ is a power of two, i.e. $k = 2^{p}$ with $0 \le p \le 20$, so $1 \le k \le 2^{20}$
- for $t = 2$: $0 \le b = x \le 59$

The answer is at most $n \le 10^{18}$, so it fits into a signed 64-bit integer. When computing with inclusion-exclusion, add the counts group by group according to the subset size (the sum of one group is about $C(m,k) \cdot n / 2^{k}$); then every intermediate value also fits into 64 bits.

### Sample explanation

Sample 1: $n = 10$ and the two conditions are "is a multiple of $2$" and "bit $1$ is $1$".

- multiples of $2$: $2, 4, 6, 8, 10$;
- numbers with bit $1$ set: $2, 3, 6, 7, 10$.

Their union is $\{2, 3, 4, 6, 7, 8, 10\}$, which has $7$ elements, so the output is `7`.

### Hint

By inclusion-exclusion,

$$\text{answer} = \sum_{\varnothing \ne T \subseteq \{1,\dots,m\}} (-1)^{|T|+1} \cdot c(T),$$

where $c(T)$ is the number of integers in $[1, n]$ satisfying every condition of $T$.

Both kinds of conditions only restrict binary digits: the divisibility condition $k = 2^{p}$ forces the low $p$ bits to be $0$ (so `zero_mask |= k - 1`), and a bit condition forces bit $b$ to be $1$ (`one_mask |= 1 << b`). Hence the constraints of a subset $T$ merge into two masks `zero_mask` and `one_mask`:

- if the masks intersect, $c(T) = 0$;
- otherwise $c(T)$ counts the integers in $[0, n]$ whose specified bits are fixed and whose other bits are free. Scan the bits from high to low: whenever the current bit of $n$ is $1$ and that bit is not forced to $1$, put a $0$ there, and every unrestricted lower bit becomes free, contributing $2^{\text{number of free bits}}$; then continue along the branch that still equals the prefix of $n$. Finally subtract $x = 0$ (it is counted exactly when `one_mask` is $0$).

Since $m \le 8$, enumerate the $2^{m} - 1 \le 255$ non-empty subsets, each costing $O(60)$.

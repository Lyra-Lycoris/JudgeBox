# Numbers with Exactly k Set Bits

Given $l, r, k$, count how many integers in the closed interval $[l, r]$ have exactly $k$ ones in their binary representation.

### Input

A single line with three integers $l, r, k$ separated by spaces.

### Output

One integer: the number of integers in the interval satisfying the condition.

### Constraints

- $1 \le l \le r \le 10^{18}$
- $0 \le k \le 60$

### Sample explanation

The integers in $[1, 16]$ with exactly one set bit are $1 = 1_2$, $2 = 10_2$, $4 = 100_2$, $8 = 1000_2$, $16 = 10000_2$, so the output is $5$.

### Hint

This is digit DP over binary digits. Let $f(x)$ be the number of integers in $[0, x]$ with exactly $k$ ones; the answer is $f(r) - f(l-1)$.

Scan the binary digits of $x$ from the most significant one while tracking `used`, the number of ones already fixed. When position $b$ is scanned (with $b$ lower positions remaining) and the bit of $x$ there is $1$, we may put $0$ there: the $b$ lower positions are free and must contain $k - used$ ones, giving $\binom{b}{k - used}$ possibilities. After adding that, follow the bit of $x$ (put $1$) and increment `used`. If `used` exceeds $k$, the remaining prefix can never be valid, so stop. At the end, if `used == k` exactly, $x$ itself is valid and contributes one more.

The binomial coefficients $\binom{b}{j}$ can be precomputed with Pascal's triangle ($b \le 60$, the largest is about $1.18 \times 10^{17}$, which fits in 64-bit integers). The total complexity is $O(60)$.

# Total Digit Sum in a Range

Let $s(x)$ be the sum of the decimal digits of $x$ (for example $s(2024) = 2 + 0 + 2 + 4 = 8$).

Given two positive integers $l$ and $r$, compute

$$\sum_{x=l}^{r} s(x)$$

that is, the total of the digit sums of all integers in the interval $[l, r]$.

### Input

A single line with two integers $l$ and $r$ separated by a space.

### Output

One integer: the total of the digit sums of the integers in the interval.

### Constraints

- $1 \le l \le r \le 10^{15}$

### Sample explanation

$s(1) + s(2) + \dots + s(9) + s(10) = 1 + 2 + \dots + 9 + 1 = 46$, so the output is $46$.

### Hint

Enumerating the integers is too slow; do dynamic programming over the **digits**. Let $f(x) = \sum_{v=0}^{x} s(v)$; the answer is $f(r) - f(l-1)$.

Scan the digits of $x$ from the most significant one. Assume we are at a position with $p$ positions to its right and that the digits fixed so far have sum `prefix`. If the current digit takes a value $v$ smaller than the digit of $x$, then:

- the prefix together with this digit contributes $(prefix + v) \times 10^{p}$, because there are $10^{p}$ possible suffixes and every one of them inherits this prefix sum;
- the $p$ remaining positions contribute $p \times 45 \times 10^{p-1}$ in total over all $10^{p}$ suffixes, since over all combinations every position takes each of $0 \sim 9$ exactly $10^{p-1}$ times.

Do not forget the digit sum of $x$ itself. The total complexity is $O(\log_{10} r)$.

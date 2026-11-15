# Construct a Permutation Maximizing the Adjacent Difference Sum

You are given an integer $n$.

Construct a permutation $p_1, p_2, \dots, p_n$ of $1, 2, \dots, n$ that makes

$$\sum_{i=1}^{n-1} \lvert p_i - p_{i+1} \rvert$$

as large as possible. You only have to print any permutation that **attains the maximum**.

This problem uses a **special judge** (SPJ): any permutation attaining the maximum is accepted.

### Input

A single line with one integer $n$.

### Output

Print $n$ integers forming a permutation of $1, \dots, n$. The numbers may be separated by spaces or newlines; you must print exactly $n$ numbers.

### Constraints

$1 \le n \le 200000$.

### Sample explanation

Sample 1: $n = 5$. The output `3 5 1 4 2` gives adjacent differences $\lvert 3-5 \rvert = 2$, $\lvert 5-1 \rvert = 4$, $\lvert 1-4 \rvert = 3$ and $\lvert 4-2 \rvert = 2$, whose sum is $11$. One can prove that $11$ is the maximum for $n = 5$ (for instance `1 2 3 4 5` only reaches $4$).

### Hint

Rewrite the sum with a coefficient for every element: the two endpoints get coefficient $\pm 1$ and every inner element gets $\pm 2$. To maximize the sum, the large values should receive $+2$ and the small ones $-2$; this gives the maximum value $\lfloor n^2/2 \rfloor - 1$ for $n \ge 2$ (and $0$ for $n = 1$).

A construction alternates large and small values: print $\lceil n/2 \rceil$ first, then alternately "the current largest unused value, the current smallest unused value", i.e. $n, 1, n-1, 2, n-2, 3, \dots$ until the permutation is complete.

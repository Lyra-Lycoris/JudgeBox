# Inversion Counting

You are given an integer sequence $a_1, a_2, \dots, a_n$. A pair of indices $(i, j)$ is called an **inversion** if $i < j$ and $a_i > a_j$.

Count the total number of inversions in the sequence.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

One integer: the number of inversions.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$
- The answer is at most $\frac{n(n-1)}{2} \le 2 \times 10^{10}$, so use 64-bit integers

### Sample explanation

The sequence is $5, 4, 3, 2, 1$. Every pair of positions forms an inversion, so the answer is $\binom{5}{2} = 10$; the output is `10`.

# Find a Peak Element

You are given an integer array $a_0, a_1, \dots, a_{n-1}$ of length $n$. All elements of the array are **distinct**.

An index $i$ is a **peak** if and only if:

- $a_i > a_{i-1}$ whenever $i > 0$;
- $a_i > a_{i+1}$ whenever $i < n - 1$.

In other words, a peak is larger than every neighbour it has. Treat the virtual elements at indices $-1$ and $n$ as $-\infty$, so the first and the last element may also be peaks.

Return the index (0-based) of **any** peak element.

This problem uses a **special judge (SPJ)**: any index that is really a peak is accepted, it does not have to match the reference answer.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_0, a_1, \dots, a_{n-1}$.

### Output

One integer $i$ ($0 \le i < n$): the index of a peak element.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$
- All elements of the array are distinct

### Sample explanation

With $n = 4$ and the array $1, 2, 3, 0$:

- Index $0$: $a_0 = 1 < a_1 = 2$, not a peak.
- Index $1$: $a_1 = 2 < a_2 = 3$, not a peak.
- Index $2$: $a_2 = 3 > a_1 = 2$ and $a_2 = 3 > a_3 = 0$, a peak.
- Index $3$: $a_3 = 0 < a_2 = 3$, not a peak.

The only peak is index $2$, so printing $2$ is correct (any other valid peak would be accepted too, but in this array none exists).

Because moving towards a larger neighbour always leads to a peak, binary search finds a peak in $O(\log n)$ time.

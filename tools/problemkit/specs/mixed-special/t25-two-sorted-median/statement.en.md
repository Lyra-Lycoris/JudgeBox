# Median of Two Sorted Arrays

You are given two **non-decreasing** integer sequences: $a_1, \dots, a_n$ and $b_1, \dots, b_m$.

Merge them into one non-decreasing sequence $S$ of length $N = n + m$ (all elements of both sequences together, sorted in non-decreasing order).

Find the sum of the two middle elements of $S$:

- if $N$ is odd there is a single middle element $S_{(N+1)/2}$, and the answer is $2 \times S_{(N+1)/2}$ (that is, twice the median);
- if $N$ is even the answer is $S_{N/2} + S_{N/2+1}$ (again twice the median).

Equivalently, with $1$-based indices the answer is $S_{\lfloor (N-1)/2 \rfloor + 1} + S_{\lfloor N/2 \rfloor + 1}$. This value is always an integer, so no fractions appear.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, \dots, a_n$ (non-decreasing).
- The third line contains one integer $m$.
- The fourth line contains $m$ integers $b_1, \dots, b_m$ (non-decreasing).

### Output

A single integer: the sum of the two middle elements of the merged sequence.

### Constraints

$1 \le n, m \le 200000$, $-10^9 \le a_i, b_j \le 10^9$.

Merging the arrays takes $O(n+m)$ time and memory. That is acceptable in C++ here, but an $O(\log \min(n,m))$ partition approach is nicer; in Python it is better to binary search the value of the answer.

### Sample explanation

Sample 1: $n = 2$ with $a = (1, 3)$, and $m = 1$ with $b = (2)$. The merged sequence is $S = (1, 2, 3)$. Its length $N = 3$ is odd and the middle element is $2$, so the answer is $2 \times 2 = 4$.

### Hint

Turn "find the $k$-th smallest" into a decision problem: binary search the value $x$ and count, with two binary searches (`upper_bound`), how many elements of $a$ and of $b$ are at most $x$. If the total is at least $k$, the $k$-th smallest value is at most $x$. The value range is only $2 \times 10^9$, so about $31$ rounds are enough and the total complexity is $O(\log V \cdot \log n)$. Compute the $\lfloor (N+1)/2 \rfloor$-th and the $\lfloor (N+2)/2 \rfloor$-th smallest values and add them.

# Median of Two Sorted Arrays

Given two **non-decreasing** integer arrays $a$ (length $n$) and $b$ (length $m$), merge them into one sorted array of length $n + m$ (duplicates are kept, no element is removed) and find its median.

Definition of the median:

- if the merged length is odd, the median is the middle element;
- if the merged length is even, the median is the average of the two middle elements.

This problem asks for **twice the median**, which is always an integer (possibly negative).

For example, $a = [1, 3]$ and $b = [2]$ merge to $[1, 2, 3]$, whose median is $2$, so the answer is $4$. Another example: $a = [1, 2]$ and $b = [3, 4]$ merge to $[1, 2, 3, 4]$, whose median is $2.5$, so the answer is $5$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1 \le a_2 \le \dots \le a_n$.
- The third line contains one integer $m$.
- The fourth line contains $m$ integers $b_1 \le b_2 \le \dots \le b_m$.

### Output

A single integer: twice the median.

### Constraints

- $1 \le n, m \le 100000$
- $|a_i|, |b_i| \le 10^9$
- both arrays are non-decreasing

The absolute value of the answer is at most $2 \times 10^9$, which fits in a 64-bit integer.

### Sample explanation

Sample 1: $a = [1, 3]$, $b = [2]$ merge to $[1, 2, 3]$, the median is $2$, so the output is `4`.

Sample 2: $a = [1, 2]$, $b = [3, 4]$ merge to $[1, 2, 3, 4]$, the median is $(2 + 3) / 2 = 2.5$, so the output is `5`.

Sample 3: $a = [-5]$, $b = [5]$ merge to $[-5, 5]$, the median is $0$, so the output is `0`.

### Hint

Let $S = n + m$ be the merged length. Twice the median equals the $(\lfloor (S-1)/2 \rfloor + 1)$-th smallest element plus the $(\lfloor S/2 \rfloor + 1)$-th smallest element (1-based).

So the task becomes finding the $k$-th smallest element of two sorted arrays. Divide and conquer: take the first $\lceil (k+1)/2 \rceil$ elements of both arrays, compare the last element of each block, and discard the block whose last element is smaller — it cannot contain the $k$-th smallest element. Then decrease $k$ accordingly and repeat until $k = 0$. At least half of the candidates are removed each round, so the complexity is $O(\log(n+m))$.

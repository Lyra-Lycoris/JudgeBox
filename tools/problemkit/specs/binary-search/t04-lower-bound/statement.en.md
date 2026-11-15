# First Position Not Less Than x

You are given a **non-decreasing** integer array $a_0, a_1, \dots, a_{n-1}$ of length $n$ and an integer $x$.

Find the smallest index $i$ ($0 \le i \le n$) such that $a_i \ge x$. If no such index exists (that is, every element is smaller than $x$), return $n$.

Array indices are $0$-based.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_0, a_1, \dots, a_{n-1}$, guaranteed to be non-decreasing ($a_0 \le a_1 \le \dots \le a_{n-1}$).

The third line contains one integer $x$.

### Output

One integer: the smallest index $i$ with $a_i \ge x$, or $n$ if no such index exists.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$, and the array is non-decreasing
- $-10^9 \le x \le 10^9$

### Sample explanation

With $n = 5$, the array is $1, 3, 5, 7, 9$ and $x = 5$.

$a_0 = 1 < 5$, $a_1 = 3 < 5$, and $a_2 = 5 \ge 5$, so the smallest valid index is $2$ and the answer is $2$.

Since the array is monotone, binary search finds the answer in $O(\log n)$ time.

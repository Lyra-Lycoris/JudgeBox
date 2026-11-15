# Maximum Non-Adjacent Sum on a Circle

You are given a circular array $a_1, a_2, \dots, a_n$: the indices wrap around, so $a_n$ and $a_1$ are adjacent.

Choose a subset of positions $S \subseteq \{1, 2, \dots, n\}$ such that no two positions of $S$ are **adjacent** (in the circular sense, so $1$ and $n$ are adjacent too), maximizing

$$\sum_{i \in S} a_i .$$

The empty subset $S = \varnothing$ (sum $0$) is allowed, hence the answer is always non-negative.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

A single line with one integer: the maximum sum.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$
- The absolute value of the answer is at most $10^{14}$
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=4$ and the array is $5, 1, 1, 5$.

- $\{1, 3\}$ gives $5 + 1 = 6$;
- $\{2, 4\}$ gives $1 + 5 = 6$;
- $\{1, 4\}$ is invalid because $a_4$ is adjacent to $a_1$.

Therefore the answer is $6$.

### Hint

Since $a_1$ and $a_n$ are adjacent, a valid subset can never contain both $1$ and $n$. Hence only two cases exist:

1. $a_n$ is not chosen: run the linear "no two adjacent" DP on $a_1, a_2, \dots, a_{n-1}$;
2. $a_1$ is not chosen: run the same DP on $a_2, a_3, \dots, a_n$.

The linear DP is $f_i = \max(f_{i-1},\ f_{i-2} + a_i)$ with $f_0 = f_{-1} = 0$.

The answer is the larger of the two values and the total complexity is $O(n)$. Take care of $n=1$ and $n=2$ (the circular adjacency) and of the empty subset.

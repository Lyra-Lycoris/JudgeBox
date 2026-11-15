# Longest Increasing Subsequence

Given a sequence of $n$ integers $a_1, a_2, \dots, a_n$.

Find the length of its **longest strictly increasing subsequence**.

A subsequence is obtained by deleting zero or more elements from the original sequence while keeping the remaining elements in their original order. Strictly increasing means every element is strictly greater than the previous one.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the length of the longest strictly increasing subsequence.

### Constraints

$1 \le n \le 200000$, $-10^9 \le a_i \le 10^9$.

A naive $O(n^2)$ dynamic programming solution will not fit in the time limit; an $O(n \log n)$ approach is required.

### Sample explanation

Sample 1: $n = 8$ and the sequence is $10, 9, 2, 5, 3, 7, 101, 18$.

The subsequence $2, 3, 7, 101$ (indices $3, 5, 6, 7$) has length $4$, and so does $2, 5, 7, 101$. No strictly increasing subsequence of length $5$ exists, so the output is `4`.

### Hint

Let $tails[k]$ be the smallest possible last element of an increasing subsequence of length $k+1$. This array is non-decreasing, so for each $a_i$ you can binary search the first position holding a value $\ge a_i$ and replace it; if every stored value is smaller than $a_i$, append $a_i$. The answer is the final length of $tails$, and the complexity is $O(n \log n)$.

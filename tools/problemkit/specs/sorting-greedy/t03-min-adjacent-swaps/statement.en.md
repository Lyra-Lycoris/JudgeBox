# Minimum Adjacent Swaps to Sort

Given an integer sequence $a_1, a_2, \dots, a_n$ of length $n$. In one operation you may swap two adjacent elements. Compute the minimum number of swaps needed to make the whole sequence non-decreasing ($a_1 \le a_2 \le \dots \le a_n$).

When the sequence contains equal elements, an optimal solution never changes their relative order (this is a stable sort); you may use this fact directly.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

One integer: the minimum number of adjacent swaps.

### Constraints

- $1 \le n \le 10^5$
- $|a_i| \le 10^9$

### Sample explanation

The sequence is $2, 4, 1, 3$. Swap $4$ and $1$ to get $2, 1, 4, 3$; swap $2$ and $1$ to get $1, 2, 4, 3$; swap $4$ and $3$ to get $1, 2, 3, 4$. That is 3 swaps, and fewer than 3 cannot sort the sequence, so the answer is 3.

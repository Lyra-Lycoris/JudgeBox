# Minimum in Rotated Sorted Array

A **strictly increasing** integer array of length $n$ has been "rotated" once: some prefix of it was moved to the end (the prefix may be empty, in which case the array is unchanged).

For example, the strictly increasing array $1, 2, 3, 4, 5$ can become $3, 4, 5, 1, 2$, or stay $1, 2, 3, 4, 5$ (no rotation).

Given the rotated array, find its minimum element. All elements of the array are **distinct**.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$: the rotated array.

### Output

One integer: the minimum element of the array.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$
- All elements are distinct
- The array is guaranteed to be a rotation of some strictly increasing array

### Sample explanation

With $n = 7$ and the array $4, 5, 6, 7, 0, 1, 2$.

It is obtained by rotating the strictly increasing array $0, 1, 2, 4, 5, 6, 7$ left by $4$ positions, so the minimum is $0$ and the answer is $0$.

The array consists of two increasing runs, so comparing the middle element with the right end tells which half contains the minimum; this yields an $O(\log n)$ solution.

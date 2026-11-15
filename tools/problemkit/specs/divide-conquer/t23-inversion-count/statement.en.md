# Inversion Count with Merge Sort

Given a sequence of $n$ integers $a_1, a_2, \dots, a_n$, a pair of indices $(i, j)$ with $i < j$ is called an **inversion** if $a_i > a_j$. Count the total number of inversions in the sequence.

For example, in $2, 3, 4, 5, 6, 1$ the value $1$ is smaller than all five values before it, so there are $5$ inversions.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the total number of inversions.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$.

The answer can be as large as $\frac{n(n-1)}{2} = 19999900000$, which exceeds the range of a 32-bit integer, so use a 64-bit integer.

### Sample explanation

Sample 1: $n = 6$ and the sequence is $2, 3, 4, 5, 6, 1$. Only $1$ forms inversions with the five values before it, so the answer is `5`.

Sample 2: $n = 5$ and the sequence is $3, 3, 3, 3, 3$. All values are equal, so there is no inversion and the answer is `0`.

Sample 3: $n = 6$ and the sequence is $6, 5, 4, 3, 2, 1$. It is strictly decreasing, so every pair of indices is an inversion: $\binom{6}{2} = 15$.

### Hint

Split the sequence in the middle and recursively count inversions inside the left half and inside the right half. Every remaining inversion has one index in the left half and the other in the right half, and these can be counted while merging the two sorted halves: whenever an element of the right half is taken, all elements still left in the left half are larger than it and form an inversion with it. The total complexity is $O(n \log n)$.

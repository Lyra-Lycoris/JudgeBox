# Sorting by Adjacent Swaps

You are given a sequence of $n$ integers $a_1, a_2, \dots, a_n$.

In one operation you may swap two **adjacent** elements $a_i$ and $a_{i+1}$; the operation costs $1$.

Find the **minimum** number of operations needed to make the sequence **non-decreasing**, i.e. $a_1 \le a_2 \le \dots \le a_n$.

The sequence may contain equal elements.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

One integer: the minimum number of operations.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$

The answer never exceeds $\dfrac{n(n-1)}{2} \le 2 \times 10^{10}$, so use a 64-bit integer.

### Sample explanation

For $n = 5$ and $a = (2, 4, 1, 3, 3)$ four operations suffice:

1. swap $4$ and $1$: $(2, 1, 4, 3, 3)$;
2. swap $2$ and $1$: $(1, 2, 4, 3, 3)$;
3. swap $4$ and the first $3$: $(1, 2, 3, 4, 3)$;
4. swap $4$ and the second $3$: $(1, 2, 3, 3, 4)$.

Fewer than four operations cannot work, so the output is `4`.

### Hint

- For a **permutation** $p$, the minimum number of adjacent swaps that turns it into $1, 2, \dots, n$ equals the number of inversions of $p$. So first determine the target permutation, then count its inversions.
- The relative order of equal elements never has to change: swapping two equal values changes nothing, so we may assume that after sorting, equal elements keep their original order. Therefore sort the pairs $(a_i, i)$ — the resulting target permutation is unique.
- Inversions can be counted in $O(n \log n)$ with a Fenwick tree (or with merge sort): insert the elements of the target permutation from left to right and, for each of them, count how many already inserted elements are larger.

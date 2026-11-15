# T-th Smallest After Merging K Sorted Lists

There are $k$ integer sequences, each of length $m$, and each sequence is sorted in non-decreasing order (think of it as a sorted linked list). Merge all $k$ sequences into one non-decreasing sequence, then find its $t$-th smallest element ($1$-based, duplicates counted).

### Input

The first line contains three integers $k$, $m$ and $t$.

Each of the next $k$ lines contains $m$ integers: one non-decreasing sequence.

### Output

Print one integer: the $t$-th smallest element of the merged sequence.

### Constraints

- $1 \le k, m \le 400$, $1 \le t \le k \times m$
- Every element has absolute value at most $10^9$
- Every line is guaranteed to be non-decreasing

### Sample Explanation

The three sequences are $[1,4,7]$, $[2,5,8]$ and $[3,6,9]$. The merged sequence is $1,2,3,4,5,6,7,8,9$, whose $5$-th smallest element is $5$.

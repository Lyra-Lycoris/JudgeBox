# Longest Consecutive Sequence

Given $n$ integers $a_1, a_2, \dots, a_n$, consider the set of distinct values they contain. Find the longest block of **consecutive integers** in this set and print the length of that block.

For example, for the value set $\{1, 2, 3, 10, 11, 12, 13\}$ the longest block is $10, 11, 12, 13$, whose length is $4$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

Print one integer: the length of the longest consecutive block.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$.

### Sample explanation

The value set of sample 1 is $\{1, 2, 3, 4, 100, 200\}$:

- $1, 2, 3, 4$ are consecutive and form a block of length $4$;
- $100$ and $200$ each form a block of length $1$.

The longest block has length $4$, so the answer is `4`.

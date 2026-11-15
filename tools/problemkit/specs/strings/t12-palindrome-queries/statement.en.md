# Palindrome Substring Queries

You are given a lowercase English string $s$ of length $n$ and $q$ queries. Each query gives two integers $l, r$ ($1 \le l \le r \le n$) and asks whether the substring $s[l..r]$ is a **palindrome** (reads the same forwards and backwards).

For example `abcba`, `aa` and `z` are palindromes, while `ab` is not.

### Input

- The first line contains one integer $n$.
- The second line contains a lowercase string $s$ of length $n$.
- The third line contains one integer $q$.
- The next $q$ lines each contain two integers $l, r$, describing one query.

### Output

Print one line with $q$ space-separated integers. The $j$-th integer is `1` if the substring of the $j$-th query is a palindrome and `0` otherwise.

### Constraints

- $1 \le n \le 2 \times 10^5$ and $1 \le q \le 2 \times 10^5$.
- $1 \le l \le r \le n$.
- $s$ consists of lowercase English letters `a` to `z` only.

### Sample explanation

Sample 1: $n = 5$, $s = \text{abcba}$, $q = 3$.

- Query $[1,5]$: `abcba` reads the same both ways, so the answer is `1`;
- query $[1,3]$: `abc` is not a palindrome, so the answer is `0`;
- query $[2,4]$: `bcb` is a palindrome, so the answer is `1`.

Hence the output is `1 0 1`.

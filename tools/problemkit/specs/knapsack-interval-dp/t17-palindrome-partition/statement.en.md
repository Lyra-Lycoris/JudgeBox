# Palindrome Partitioning Minimum Cuts

Given a string $s$ of lowercase letters, split it into contiguous substrings so that every substring is a palindrome. Return the minimum number of cuts needed.

For example `aab` can be split into `aa` and `b` with $1$ cut, or into `a`, `a`, `b` with $2$ cuts, so the answer is $1$.

### Input

- One line with the string $s$, containing only lowercase letters and no spaces.

### Output

One integer: the minimum number of cuts. If $s$ is already a palindrome the answer is $0$.

### Constraints

$1 \le |s| \le 1500$.

### Sample explanation

Sample 1: $s = $ `aab`. Cutting into `aa` and `b` gives two palindromes using $1$ cut, and with $0$ cuts `aab` is not a palindrome, so the minimum is $1$.

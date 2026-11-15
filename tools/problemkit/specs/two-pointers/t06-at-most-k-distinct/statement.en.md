# Longest Substring with At Most K Distinct Characters

Given a string $s$ of English letters and digits and a non-negative integer $k$, find the longest contiguous substring of $s$ that contains **at most $k$ distinct characters**, and print its length.

When $k = 0$, every non-empty substring contains at least one distinct character, so the answer is $0$.

### Input

The first line contains one integer $k$.

The second line contains a non-empty string $s$ made of lowercase letters, uppercase letters and digits.

### Output

One integer: the maximum length of a substring with at most $k$ distinct characters.

### Constraints

- $0 \le k \le 62$
- $1 \le |s| \le 200000$
- $s$ contains only `a`–`z`, `A`–`Z` and `0`–`9`

### Sample explanation

Sample 1: $k = 2$, $s = \texttt{eceba}$. The substring `ece` uses only `e` and `c` and has length $3$; any longer substring would introduce a third character, so the answer is $3$.

Sample 2: $k = 1$, $s = \texttt{aaabbb}$. The longest single-character substrings are `aaa` and `bbb`, of length $3$.

Sample 3: $k = 0$, no character is allowed, so the answer is $0$.

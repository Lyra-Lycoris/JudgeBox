# Longest Substring Without Repeating Characters

Given a string $s$ that contains only English letters and digits, find the longest **contiguous substring** in which no character appears twice, and print the length of that substring.

A substring is a contiguous segment of the original string. Only the maximum length matters here.

### Input

One line with a non-empty string $s$ made of lowercase letters, uppercase letters and digits.

### Output

One integer: the length of the longest substring without repeating characters.

### Constraints

- $1 \le |s| \le 200000$, where $|s|$ is the length of the string.
- $s$ contains only `a`–`z`, `A`–`Z` and `0`–`9`.

### Sample explanation

Sample 1: `abcabcbb`. The longest substring with all distinct characters is `abc`, so the answer is $3$.

Sample 2: `bbbbb`. Every substring of length greater than $1$ repeats a character, so the answer is $1$.

Sample 3: `pwwkew`. The longest such substrings are `wke` and `kew`, both of length $3$; `pwke` is only a subsequence, not a substring.

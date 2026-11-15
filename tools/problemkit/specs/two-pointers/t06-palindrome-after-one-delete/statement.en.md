# Valid Palindrome After Deleting At Most One Character

Given a string $s$ that contains only lowercase English letters, you may delete **at most** one character (deleting nothing is also allowed). Decide whether the result can be a palindrome.

A palindrome reads the same forwards and backwards; the empty string and strings of length $1$ are palindromes.

### Input

One line with a non-empty string $s$ of lowercase letters.

### Output

Print `YES` if $s$ can become a palindrome after deleting at most one character, otherwise print `NO`.

### Constraints

- $1 \le |s| \le 200000$
- $s$ contains only `a`–`z`

### Sample explanation

Sample 1: `aba` is already a palindrome, so nothing has to be deleted and the answer is `YES`.

Sample 2: deleting `b` (or `c`) from `abca` gives `aca` (or `aba`), which is a palindrome, so the answer is `YES`.

Sample 3: deleting any single character of `abc` leaves two different characters, so no palindrome is possible and the answer is `NO`.

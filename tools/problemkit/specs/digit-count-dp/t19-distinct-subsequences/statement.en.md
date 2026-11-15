# Count Distinct Subsequences

You are given a string $s$ of length $n$ consisting of lowercase English letters only.

A subsequence is obtained by deleting some (possibly zero) characters from $s$ and keeping the remaining characters in their original relative order. Two subsequences are considered the same if their contents are equal, even when they come from different positions. Count the number of **distinct non-empty subsequences** of $s$ modulo $10^9+7$.

### Input

The first line contains one integer $n$.

The second line contains a string $s$ of length $n$ (lowercase English letters, no spaces).

### Output

One integer: the number of distinct non-empty subsequences modulo $10^9+7$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $s$ consists of the lowercase letters `a`~`z`

### Sample explanation

For $s = \texttt{aba}$ the non-empty subsequences are `a`, `b`, `ab`, `aa`, `ba`, `aba`, i.e. $6$ different ones, so the output is $6$. Note that the first `a` and the last `a` both produce the same single-character subsequence `a`.

### Hint

First allow the empty string. Let $dp[i]$ be the number of distinct subsequences (including the empty one) of the length-$i$ prefix of $s$, with $dp[0] = 1$. Without deduplication, character $c$ at position $i$ would give $2\,dp[i-1]$ possibilities (append $c$ to each old subsequence or not). But if $c$ already appeared at position $p$ (1-based), the subsequences formed by appending $c$ at $p$ are counted twice, and there are exactly $dp[p-1]$ of them. Hence

$$dp[i] = 2\,dp[i-1] - [\,c \text{ appeared before}\,] \cdot dp[p-1]$$

Keep an array of size $26$ storing the last occurrence of every letter. The complexity is $O(n)$ time and $O(n)$ space. Finally subtract the empty string: the answer is $dp[n] - 1$.

Since a subtraction modulo $10^9+7$ can be negative, add $10^9+7$ before taking the modulo again.

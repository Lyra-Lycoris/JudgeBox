# Longest Common Subsequence

Given two strings $s$ and $t$ consisting of lowercase English letters.

Find the length of their **longest common subsequence**.

A subsequence is obtained by deleting zero or more characters from a string while keeping the remaining characters in their original order. A common subsequence is a string that is a subsequence of both $s$ and $t$.

### Input

- The first line contains a non-empty string $s$.
- The second line contains a non-empty string $t$.

The strings contain no spaces and consist only of lowercase English letters.

### Output

A single integer: the length of the longest common subsequence.

### Constraints

$1 \le |s|, |t| \le 2000$.

### Sample explanation

Sample 1: $s = \texttt{abcde}$ and $t = \texttt{ace}$.

The string $\texttt{ace}$ is a subsequence of both $s$ and $t$ and has length $3$. Since $t$ has only $3$ characters, no longer common subsequence exists, so the output is `3`.

### Hint

Let $f_{i,j}$ be the length of the longest common subsequence of the first $i$ characters of $s$ and the first $j$ characters of $t$. Then

$$f_{i,j} = \begin{cases} f_{i-1,j-1} + 1, & s_i = t_j \\ \max(f_{i-1,j},\ f_{i,j-1}), & s_i \ne t_j \end{cases}$$

with $f_{0,j} = f_{i,0} = 0$. The answer is $f_{|s|,|t|}$, and a rolling array reduces the memory to $O(|t|)$.

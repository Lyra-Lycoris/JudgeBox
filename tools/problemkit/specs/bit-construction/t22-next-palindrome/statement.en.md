# Next Palindrome

An integer is a **palindrome** if its decimal representation (without leading zeros) reads the same from left to right and from right to left. For example $0, 7, 11, 121, 1331, 9999$ are palindromes, while $10, 123, 1000$ are not.

Given a non-negative integer $n$, find the smallest palindrome that is **greater than or equal to** $n$.

### Input

A single line with one integer $n$.

### Output

A single line with one integer: the smallest palindrome $\ge n$.

### Constraints

- $0 \le n \le 10^{18}$.

The answer never exceeds $1000000000000000001$ ($10^{18}+1$) and fits into a 64-bit integer.

### Sample explanation

**Sample 1**: $n = 1234$.

$1234$ itself is not a palindrome. A palindrome with the same number of digits is fully determined by its first half:

- with first half $12$ the palindrome is $1221 < 1234$;
- with first half $13$ the palindrome is $1331 \ge 1234$.

So the smallest palindrome $\ge 1234$ is $1331$, and the output is `1331`.

**Sample 2**: $n = 102$.

$n$ has three digits, so its first half (including the middle digit) is $10$ and mirroring gives $101 < 102$. Incrementing the half gives $11$, and mirroring gives $111 \ge 102$, so the output is `111`.

### Hint

Let $n$ have $L$ digits and let $h$ be the first $\lceil L/2 \rceil$ digits of $n$ (including the middle digit when $L$ is odd).

1. Append the reverse of $h$ to $h$ to obtain a candidate $c$: for even $L$ append the whole reversed $h$, for odd $L$ drop the first character of the reversed $h$ (that character is the middle digit).
2. If $c \ge n$, then $c$ is the answer.
3. Otherwise the next palindrome with the same number of digits is obtained by mirroring $h+1$ (if $h+1$ has more digits than $h$, then $n$ was of the form $99\cdots9$ and the answer is $1$, then $L-1$ zeros, then $1$).

The whole procedure takes $O(L)$ time with $L \le 19$.

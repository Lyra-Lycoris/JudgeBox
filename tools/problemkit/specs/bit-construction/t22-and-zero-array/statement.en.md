# Construct an Array with Zero Adjacent AND

Given an integer $n$, construct a sequence of $n$ integers $a_1, a_2, \dots, a_n$ such that:

1. $1 \le a_i \le 10^9$ for every $1 \le i \le n$;
2. $a_i \mathrel{\&} a_{i+1} = 0$ for every $1 \le i < n$, where $\&$ denotes bitwise AND.

This problem uses a **special judge (SPJ)**: any sequence satisfying the two conditions above is accepted, it does not have to match the reference solution.

### Input

A single line with one integer $n$.

### Output

One line with $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

When $n = 1$, any integer $1 \le a_1 \le 10^9$ is accepted.

### Constraints

- $1 \le n \le 200000$.

The given limits always admit a solution.

### Sample explanation

**Sample 1**: $n = 4$. The output `1 2 1 2` satisfies

- $1 \mathrel{\&} 2 = 0$;
- $2 \mathrel{\&} 1 = 0$;
- $1 \mathrel{\&} 2 = 0$.

All three adjacent pairs are fine and $1, 2$ both lie in $[1, 10^9]$, so this is a correct answer. Other valid sequences such as `4 8 1 6` are also accepted.

**Sample 2**: $n = 1$. Output any integer in $[1, 10^9]$, for example `1`.

### Hint

The condition only involves **adjacent** elements, so no global bit conflict has to be resolved: it is enough to alternate two values whose bitwise AND is $0$. Put $1$ on odd positions and $2$ on even positions.

Since $1 = (1)_2$ and $2 = (10)_2$ share no set bit, $1 \mathrel{\&} 2 = 0$, hence every adjacent pair is valid.

If you want more distinct values, let all numbers use only a few fixed bit ranges, for example alternate "numbers below $2^{20}$" with "numbers whose set bits lie in bits $20 \sim 29$"; their pairwise AND is still $0$.

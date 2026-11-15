# Distinct Numbers with Zero Adjacent AND

Given an integer $n$, construct a sequence of $n$ integers $a_1, a_2, \dots, a_n$ that satisfies all three conditions below:

1. pairwise distinct: $i \ne j \implies a_i \ne a_j$;
2. range: $1 \le a_i \le 10^{18}$ for every $i$;
3. zero adjacent AND: $a_i \mathrel{\&} a_{i+1} = 0$ for every $1 \le i < n$,

where $\&$ denotes bitwise AND.

This problem uses a **special judge (SPJ)**: any sequence satisfying the three conditions is accepted, it does not have to match the reference solution.

### Input

A single line with one integer $n$.

### Output

One line with $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

When $n = 1$, output any integer with $1 \le a_1 \le 10^{18}$.

### Constraints

- $1 \le n \le 200000$.

The given limits always admit a solution.

### Sample explanation

**Sample 1**: $n = 4$. A valid output is `1 1099511627776 2 2199023255552`.

- The four numbers are pairwise distinct;
- they are $1$, $2^{40}$, $2$, $2 \cdot 2^{40}$, all inside $[1, 10^{18}]$;
- $1 \mathrel{\&} 2^{40} = 0$, $2^{40} \mathrel{\&} 2 = 0$, $2 \mathrel{\&} (2 \cdot 2^{40}) = 0$.

Hence this is a correct answer; other valid sequences are accepted as well.

**Sample 2**: for $n = 1$ there is no adjacency constraint, so `1` is fine.

### Hint

If only the zero-AND condition were required, `1 2 1 2 ...` would suffice. Here, however, all numbers must be **pairwise distinct**, and alternating small numbers repeats very soon.

A key observation: if all set bits of $x$ lie among the low $17$ bits and all set bits of $y$ lie at bit $40$ or above, then $x \mathrel{\&} y = 0$ automatically. So split the numbers into two bit ranges:

- **low group**: $1, 2, 3, \dots$ (all below $2^{17}$);
- **high group**: $1 \ll 40, 2 \ll 40, 3 \ll 40, \dots$ (each value shifted left by $40$).

Alternate between the groups: $a_1 = 1,\ a_2 = 1 \ll 40,\ a_3 = 2,\ a_4 = 2 \ll 40,\ \dots$

- adjacent elements come from different groups, so their AND is $0$;
- values inside a group are distinct and the two groups occupy disjoint bit ranges, so all numbers are pairwise distinct;
- the largest value is $\lceil n/2 \rceil \ll 40$, which for $n \le 200000$ is about $1.1 \times 10^{17} < 10^{18}$.

This also explains the generous $10^{18}$ bound: with an upper bound of only $10^9$ neither bit range could supply $10^5$ distinct values, and such a construction would be impossible.

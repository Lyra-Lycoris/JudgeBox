# Guess the Code from Hints

There is a secret code of length $n$. Every position holds a digit from $0$ to $9$; digits may repeat and leading zeros are allowed.

You are given $k$ guesses. Each guess comes with two hints:

- $A$: the number of positions where both the digit and its position are correct;
- $B$: the number of digits that occur in the code but at a different position. Concretely, treat the code and the guess as multisets of digits: the total number of common digits (counted with the smaller multiplicity) minus $A$ gives $B$.

It is guaranteed that exactly one code satisfies all the hints. Find it.

### Input

The first line contains two integers $n$ and $k$, separated by a space.

The second line contains $k$ guesses; each guess is a string of $n$ digits (it may start with `0`). They are separated by spaces.

The third line contains $k$ integers $A_1, \dots, A_k$, separated by spaces.

The fourth line contains $k$ integers $B_1, \dots, B_k$, separated by spaces.

### Output

Print one line with $n$ integers — the digits of the code — separated by single spaces.

### Constraints

- $1 \le n \le 4$
- $1 \le k \le 20$
- $0 \le A_i, B_i \le n$ and $A_i + B_i \le n$
- Exactly one code satisfies all the hints
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3 3
123 720 247
1 1 1
0 1 2
```

**Output**

```
4 2 7
```

### Sample explanation

Here $n = 3$ and the three records are:

| Guess | $A$ | $B$ | Meaning |
|---|---|---|---|
| `123` | 1 | 0 | the `2` in position 2 is correct; `1` and `3` are not in the code |
| `720` | 1 | 1 | the `2` in position 2 is correct; `7` is in the code but misplaced |
| `247` | 1 | 2 | the `7` in position 3 is correct; `2` and `4` are in the code but misplaced |

The only code satisfying every hint is `4 2 7`, so the output is `4 2 7`.

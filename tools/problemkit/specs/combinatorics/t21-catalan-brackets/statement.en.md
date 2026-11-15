# Counting Valid Bracket Sequences

Using $n$ pairs of brackets one can build bracket strings of length $2n$. A bracket string is **valid** if and only if, scanning from left to right, the number of opening brackets is never smaller than the number of closing brackets, and at the end the two counts are equal.

Count the valid bracket strings of length $2n$, modulo $10^9+7$.

For $n = 3$ there are $5$ valid strings:

```
((()))  (()())  (())()  ()(())  ()()()
```

### Input

A single integer $n$.

### Output

One integer: the number of valid bracket strings modulo $10^9+7$.

### Constraints

- $0 \le n \le 200000$
- For $n = 0$ the empty string is the only possibility, so the answer is $1$

### Sample explanation

Sample 1: $n = 3$; the five valid strings are listed above, so the answer is $5$.

Sample 2: $n = 0$; the empty string is the only option, so the answer is $1$.

# Maximum Expression Value by Parenthesizing

You are given an expression built from $m$ non-negative integers and $m - 1$ operators, where every operator is one of `+`, `-`, `*`. For example, with $m = 3$, numbers $(1, 2, 3)$ and operators `+`, `*`, the expression is $1 + 2 * 3$.

You may insert parentheses anywhere to change the evaluation order (every full parenthesization is allowed), but you must not reorder the numbers or the operators. Find the maximum value over all valid parenthesizations.

### Input

- The first line contains one integer $m$.
- The second line contains $m$ integers: the numbers of the expression.
- The third line contains $m - 1$ characters: the operators, each one of `+`, `-`, `*` (this line is absent when $m = 1$).

Numbers and operators are separated by single spaces.

### Output

One integer: the maximum achievable value.

### Constraints

$1 \le m \le 15$, and every number is between $0$ and $9$. The absolute value of the answer does not exceed $9^{15}$, which fits in a 64-bit integer.

### Sample explanation

Sample 1: $m = 3$, numbers $(1, 2, 3)$, operators `+`, `*`, so the expression is $1 + 2 * 3$. The two parenthesizations are $(1 + 2) * 3 = 9$ and $1 + (2 * 3) = 7$; the maximum is $9$.

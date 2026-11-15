# Infix Expression Evaluation

You are given a valid infix arithmetic expression containing only non-negative integer literals, the binary operators `+`, `-`, `*`, `/` and parentheses. Evaluate it.

Rules:

- The usual precedence applies: `*` and `/` bind tighter than `+` and `-`, and operators of the same precedence associate from left to right.
- Parentheses override the default order.
- Division truncates toward zero, so `7/2 = 3` and `(0-7)/2 = -3` (rounding toward zero, not down).
- There is no unary minus: `-` only appears as a binary subtraction, and two operators are never adjacent.
- The expression contains no spaces.

### Input

One line with a valid infix expression of at most $200000$ characters.

### Output

One integer: the value of the expression.

### Constraints

The length $L$ satisfies $1 \le L \le 200000$, and every integer literal is at most $10^9$. Division by zero never happens, and every intermediate result (including the final answer) has absolute value at most $10^{15}$, so a 64-bit integer is enough.

### Sample explanation

Sample 1: `(1+2)*3`. The parenthesised part is $3$, multiplied by $3$ gives $9$.

Sample 2: `(3-10)/2`. First $3-10=-7$, then $-7/2$ truncates toward zero, giving $-3$ (rounding down would give $-4$, which is not what this problem asks for).

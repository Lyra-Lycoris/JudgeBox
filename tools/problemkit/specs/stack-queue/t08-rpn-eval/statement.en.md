# Evaluate Reverse Polish Notation

Reverse Polish notation (postfix notation) writes every operator after its two operands. For example, the infix expression $(3 + 4) \times 2$ becomes `3 4 + 2 *` in postfix form.

You are given a valid reverse Polish expression. Every token is either

- an integer (possibly negative, for example `-7`), or
- one of the operators `+`, `-`, `*`, `/`.

Here `/` is integer division that **truncates toward zero** (for example `-7 / 2 = -3` and `6 / -4 = -1`).

### Input

- The first line contains one integer $k$, the number of tokens.
- The next $k$ tokens are separated by whitespace (spaces or line breaks).

### Output

One integer: the value of the expression.

### Constraints

- $1 \le k \le 200000$, and $k$ is odd;
- the absolute value of every integer in the input is at most $10^9$;
- the expression is valid: every operator has enough operands and no division by zero happens;
- the absolute value of every intermediate result and of the final answer is at most $10^9$.

### Sample explanation

Sample 1: the tokens are `3`, `4`, `+`, `2`, `*`. First `3 + 4 = 7`, then `7 * 2 = 14`, so the answer is `14`.

Sample 2: the tokens are `-7`, `2`, `/`. Division truncates toward zero, so $-7 / 2 = -3.5$ becomes $-3$ and the answer is `-3`.

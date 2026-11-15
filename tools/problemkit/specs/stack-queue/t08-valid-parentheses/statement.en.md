# Valid Bracket Sequence

You are given a string $s$ made only of the six characters `(`, `)`, `[`, `]`, `{`, `}`. Decide whether $s$ is a valid bracket sequence.

A valid bracket sequence is defined as follows:

- the empty string is valid;
- if $A$ is valid, then `(` $A$ `)`, `[` $A$ `]` and `{` $A$ `}` are valid;
- if $A$ and $B$ are valid, then $AB$ is valid.

### Input

One line containing the string $s$, made of bracket characters only.

### Output

Print one line `YES` if $s$ is a valid bracket sequence, otherwise print `NO`.

### Constraints

- $1 \le |s| \le 200000$;
- $s$ contains only `(`, `)`, `[`, `]`, `{`, `}`.

### Sample explanation

Sample 1: `()[]{}` is the concatenation of the three valid sequences `()`, `[]` and `{}`, so the answer is `YES`.

Sample 2: in `([)]` the opening bracket `[` faces the closing bracket `)`, so the nesting is crossed and the answer is `NO`.

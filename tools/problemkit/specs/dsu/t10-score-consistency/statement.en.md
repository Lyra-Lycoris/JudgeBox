# Consistent Score Differences

There are $n$ students numbered $1 \sim n$. Each student has a score, and a score can be any integer (negative scores are allowed and there is no upper bound).

You are given $k$ statements. The $i$-th statement says "student $a_i$ scores exactly $c_i$ more than student $b_i$", i.e.

$$score_{a_i} - score_{b_i} = c_i$$

where $c_i$ may be negative, meaning $a_i$ actually scores $|c_i|$ less than $b_i$.

Determine whether there is a set of scores satisfying all $k$ statements simultaneously.

### Input

- The first line contains two integers $n$ and $k$, separated by a single space.
- Each of the next $k$ lines contains three integers $a_i, b_i, c_i$: one statement.

### Output

Print `YES` on a single line if such scores exist, otherwise print `NO`.

### Constraints

$1 \le n \le 200000$, $0 \le k \le 200000$, $1 \le a_i, b_i \le n$, $-10^9 \le c_i \le 10^9$.

It is allowed that $a_i = b_i$ (then the statement requires $c_i = 0$). The same statement may be given more than once.

### Sample explanation

Sample 1: $n = 4$, $k = 3$ with statements $score_1 - score_2 = 3$, $score_2 - score_3 = -1$ and $score_1 - score_3 = 2$.

Adding the first two gives $score_1 - score_3 = 3 + (-1) = 2$, which matches the third statement exactly. Taking $score_3 = 0$, $score_2 = -1$, $score_1 = 2$ and any value (say $0$) for the unconstrained student $4$ satisfies every statement, so the answer is `YES`.

If the third statement were $score_1 - score_3 = 5$ instead, it would contradict the value $2$ implied by the first two statements, and the answer would be `NO`.

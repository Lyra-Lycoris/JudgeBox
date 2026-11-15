# Circular Combination Lock

A combination lock has $4$ dials, each showing a digit from $0$ to $9$. The dials are circular: the next value after $9$ is $0$, and the previous value before $0$ is $9$.

One operation turns any single dial one step up or one step down.

You are given the starting lock state `start`, the target state `target`, and a list of "dead" states that the lock must never show. Compute the minimum number of operations needed to turn `start` into `target`, or print `-1` if it is impossible.

The checks are applied in this order:

1. If `start` or `target` is itself a dead state, print `-1`;
2. otherwise, if `start` equals `target`, print `0`;
3. otherwise turn the dials as described, never showing a dead state.

### Input

- The first line contains a 4-character digit string: `start`.
- The second line contains a 4-character digit string: `target`.
- The third line contains an integer $n$, the number of dead states.
- If $n > 0$, the fourth line contains the $n$ dead states, separated by single spaces. If $n = 0$, there is no fourth line.

Digit strings may have leading zeros.

### Output

One integer: the minimum number of operations, or `-1`.

### Constraints

$0 \le n \le 500$. Every digit string has exactly $4$ characters, all from `0` to `9`.

### Sample explanation

Sample 1: starting from `0000` one shortest route is `0000 -> 1000 -> 1100 -> 1200 -> 1201 -> 1202 -> 0202`, which takes $6$ steps and never shows a dead state, so the answer is `6`.

Sample 2: `0000` differs from `9000` in the first dial only, and one step down from $0$ is $9$, so the answer is `1`.

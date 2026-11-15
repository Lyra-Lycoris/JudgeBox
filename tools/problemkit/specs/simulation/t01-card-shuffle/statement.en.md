# Repeated Card Shuffle

There are $n$ cards numbered $1 \sim n$. Initially card $i$ is at position $i$.

A permutation $p$ of $1 \sim n$ defines one shuffle: after the shuffle, the card that was at position $i$ is at position $p_i$ (all cards move simultaneously, so after the shuffle every position still holds exactly one card).

Apply this shuffle exactly $k$ times and output the card number at each position $1, 2, \dots, n$ in the final state.

Note that $k$ can be extremely large, so simulating all $k$ shuffles is too slow. The shuffle is a permutation, so the cards split into cycles; the cycle lengths let you jump ahead quickly.

### Input

- The first line contains two integers $n$ and $k$, separated by a single space.
- The second line contains $n$ integers $p_1, p_2, \dots, p_n$, separated by single spaces.

### Output

One line with $n$ integers: the card numbers at positions $1$ to $n$ in the final state, separated by single spaces.

### Constraints

$1 \le n \le 200000$, $0 \le k \le 10^{18}$, and $p$ is a permutation of $1 \sim n$.

### Sample explanation

Sample 1: $n = 4$, $k = 1$, $p = (2, 3, 4, 1)$. After one shuffle, card $1$ moves from position $1$ to position $2$, card $2$ to position $3$, card $3$ to position $4$, and card $4$ to position $1$. The final sequence is `4 1 2 3`.

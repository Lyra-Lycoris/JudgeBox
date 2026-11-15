# Misere Nim

There are $n$ piles of stones; the $i$-th pile contains $a_i$ stones.

Two players move alternately, the **first player** starts. On each turn the player must pick a **non-empty** pile and remove **any positive number** of stones from it (the whole pile may be emptied).

The winning condition is reversed compared with ordinary Nim:

> **The player who removes the last stone loses.**

In other words, whoever performs the move that makes every pile empty loses. The total number of stones is finite, so the game always ends and there are no draws.

Given the initial position, decide whether the **first player wins**.

### Input

- The first line contains one integer $n$, the number of piles.
- The second line contains $n$ positive integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

- Print `YES` on one line if the first player wins;
- otherwise print `NO` on one line.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le a_i \le 10^9$

### Sample explanation

For $n = 2$ with two piles of one stone each, the first player empties one of the piles. Only one pile with a single stone is left, and the second player has no choice but to take that last stone, which loses. Hence the first player wins and the output is `YES`.

### Hint

Let $x = a_1 \oplus a_2 \oplus \dots \oplus a_n$ (bitwise XOR).

- If every pile has exactly $1$ stone, the game lasts exactly $n$ moves, and the person making move $n$ takes the last stone. So the **first player wins if and only if $n$ is even**.
- Otherwise (at least one pile has more than $1$ stone), the **first player wins if and only if $x \ne 0$**, exactly as in ordinary Nim.

So only the "all piles equal to $1$" case needs a special check; in every other case just compute the XOR.

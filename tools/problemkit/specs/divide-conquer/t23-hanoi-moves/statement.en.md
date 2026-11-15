# Minimum Moves for the Tower of Hanoi

There are three pegs labelled A, B and C. Initially peg A holds $n$ disks, with radii strictly decreasing from bottom to top (the largest disk is at the bottom).

In one move you may take the top disk of one peg and put it on another peg, but a larger disk may never be placed on top of a smaller one. Find the minimum number of moves needed to move all $n$ disks from peg A to peg C.

### Input

One integer $n$.

### Output

A single integer: the minimum number of moves.

### Constraints

$1 \le n \le 60$.

The answer is at most $2^{60} - 1 = 1152921504606846975$, which fits in a signed 64-bit integer but exceeds the range of a 32-bit integer.

### Sample explanation

Sample 1: $n = 1$. Move the only disk from A to C: `1` move.

Sample 2: $n = 3$. Seven moves are necessary: move the top two disks to peg B (3 moves), move the largest disk to C (1 move), then move the two disks from B to C (3 moves), for $3 + 1 + 3 = 7$ moves.

Sample 3: $n = 60$ and the answer is $2^{60} - 1 = 1152921504606846975$.

### Hint

Let $T(n)$ be the minimum number of moves for $n$ disks. Before moving the largest disk, the $n-1$ smaller disks must be moved to the auxiliary peg ($T(n-1)$ moves); then the largest disk moves (1 move); finally the $n-1$ disks are moved onto the target peg ($T(n-1)$ moves). Hence

$$T(n) = 2T(n-1) + 1,\qquad T(1) = 1,$$

which gives $T(n) = 2^n - 1$.

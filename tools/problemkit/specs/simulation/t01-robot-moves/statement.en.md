# Robot Command Simulation

A robot starts at the point $(0, 0)$ facing north (the positive $y$ direction).

It executes a command string in order. Each character means:

- `L`: turn left by $90^\circ$ in place (no movement);
- `R`: turn right by $90^\circ$ in place (no movement);
- `F`: move one cell forward;
- `B`: move one cell backward (the facing direction does not change).

Find the robot's position after all commands are executed.

### Input

One line with a string consisting of the characters `L`, `R`, `F` and `B`, at most $200000$ characters long.

### Output

One line with two integers $x$ and $y$, separated by a single space: the final coordinates.

### Constraints

$1 \le |s| \le 200000$, where $|s|$ is the length of the command string. The final coordinates satisfy $-200000 \le x, y \le 200000$.

### Sample explanation

Sample 1: `FFRFF` — the robot walks north to $(0,2)$, turns right to face east and walks to $(2,2)$, so the answer is `2 2`.

Sample 2: `RRFF` — after two right turns the robot faces south and walks to $(0,-2)$, so the answer is `0 -2`.

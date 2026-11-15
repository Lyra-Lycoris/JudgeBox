# Shortest Path in a Maze

You are given an $n \times m$ maze. A cell containing `0` is walkable, and a cell containing `1` is a wall.

You start at the top-left cell $(0, 0)$. In one move you may step up, down, left or right by one cell; you may neither leave the maze nor step onto a wall. Find the minimum number of moves needed to reach the bottom-right cell $(n-1, m-1)$.

If the start cell or the target cell is a wall, or the target cannot be reached, return $-1$.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $n$ lines each contain $m$ integers (`0` or `1`) separated by single spaces, describing the maze.

### Output

Print one integer: the minimum number of moves from the top-left cell to the bottom-right cell, or `-1` if it is impossible.

### Constraints

- $1 \le n, m \le 500$
- Every cell of the maze is either `0` or `1`
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3 5
0 0 1 0 0
0 0 1 0 0
0 0 0 0 0
```

**Output**

```
6
```

### Sample explanation

The maze looks like this (`#` marks a wall):

```
. . # . .
. . # . .
. . . . .
```

The Manhattan distance from $(0,0)$ to $(2,4)$ is $2 + 4 = 6$, so no route can be shorter than $6$ moves. The route $(0,0) \to (1,0) \to (2,0) \to (2,1) \to (2,2) \to (2,3) \to (2,4)$ uses exactly $6$ moves, so the answer is `6`.

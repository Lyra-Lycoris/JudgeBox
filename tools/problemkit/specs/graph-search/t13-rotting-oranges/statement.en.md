# Rotting Oranges

You are given an $n \times m$ grid. Every cell holds one of three values:

- `0`: an empty cell with no orange;
- `1`: a fresh orange;
- `2`: a rotten orange.

Every minute, all rotten oranges simultaneously turn their **up, down, left and right** neighbours that hold fresh oranges into rotten oranges (an orange that just became rotten can only infect others on the next minute); rot never crosses an empty cell.

Find the minimum number of minutes until no fresh orange is left. If it is impossible to rot every fresh orange, return $-1$; if there is no fresh orange at all in the beginning, return $0$.

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $n$ lines each contain $m$ integers (`0`, `1` or `2`) separated by single spaces.

### Output

Print one integer: the minimum number of minutes needed to rot all fresh oranges, `-1` if that is impossible, or `0` if there are no fresh oranges initially.

### Constraints

- $1 \le n, m \le 500$
- Every cell is `0`, `1` or `2`
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3 3
2 1 1
1 1 0
0 1 1
```

**Output**

```
4
```

### Sample explanation

Only the top-left orange is rotten at the beginning.

- Minute $1$: $(0,1)$ and $(1,0)$ rot;
- minute $2$: $(1,1)$ rots;
- minute $3$: $(2,1)$ rots (the cell $(1,2)$ is empty);
- minute $4$: $(2,2)$ rots.

No fresh orange is left after $4$ minutes, so the answer is `4`.

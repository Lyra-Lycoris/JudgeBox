# Smallest Cyclic Rotation

You are given a sequence of $n$ integers $a_1, a_2, \dots, a_n$.

Glue the sequence into a circle and read $n$ numbers clockwise starting from any position $s$ ($1 \le s \le n$). This gives a **cyclic rotation**

$$b^{(s)} = \left(a_s,\ a_{s+1},\ \dots,\ a_n,\ a_1,\ \dots,\ a_{s-1}\right),$$

where indices larger than $n$ wrap back to $1$. There are $n$ starting positions, hence $n$ cyclic rotations (some of them may coincide as sequences).

Find the **lexicographically smallest** of those $n$ rotations and output it.

Two sequences of the same length are compared lexicographically: scan from the first position, and the first position where they differ decides — the sequence with the smaller value there is smaller.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

One line with $n$ integers: the lexicographically smallest cyclic rotation, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$

### Sample explanation

For $n = 6$ and $a = (3, 1, 4, 1, 5, 9)$ the six rotations are

$$
\begin{aligned}
&(3,1,4,1,5,9)\\
&(1,4,1,5,9,3)\\
&(4,1,5,9,3,1)\\
&(1,5,9,3,1,4)\\
&(5,9,3,1,4,1)\\
&(9,3,1,4,1,5)
\end{aligned}
$$

The smallest one starts at position $2$ and equals $(1,4,1,5,9,3)$. Among the two rotations that begin with $1$, the second element decides: $4 < 5$.

So the output is `1 4 1 5 9 3`.

### Hint

Trying all starting positions and comparing element by element costs $O(n^2)$ time, which is too slow for $n = 2 \times 10^5$. Keep two candidate starts $i, j$ together with the number $k$ of already matched positions, and skip whole blocks of impossible starts at once to obtain a linear number of comparisons.

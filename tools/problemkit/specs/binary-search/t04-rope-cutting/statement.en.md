# Cutting Ropes

There are $n$ ropes; the $i$-th rope has length $a_i$ centimetres. You must cut exactly $k$ pieces of equal length out of these ropes. Every piece must have an integer length in centimetres, and leftover scraps may be thrown away.

Find the maximum possible length of each piece. If $k$ pieces of length $1$ centimetre cannot be produced either, output $0$.

Note that each rope is cut into whole pieces only; leftovers of different ropes cannot be joined together.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$: the length of every rope in centimetres.

The third line contains one integer $k$.

### Output

One integer: the maximum length of the $k$ equal pieces, or $0$ if $k$ pieces cannot be produced.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le a_i \le 10^9$
- $1 \le k \le 10^9$

### Sample explanation

With $n = 4$, rope lengths $8, 7, 6, 5$ and $k = 4$:

- For pieces of length $5$: the ropes yield $1, 1, 1, 1$ pieces, $4$ in total, which is enough.
- For pieces of length $6$: the ropes yield $1, 1, 1, 0$ pieces, $3$ in total, which is not enough.

Hence the maximum length is $5$ and the answer is $5$.

In general, for a fixed piece length $L$ the total number of pieces is $\sum_i \lfloor a_i / L \rfloor$. This count never increases as $L$ grows, so the answer can be found by binary searching $L$.

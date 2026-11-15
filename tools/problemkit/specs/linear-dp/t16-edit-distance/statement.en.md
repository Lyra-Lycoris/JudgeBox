# Edit Distance

Given two strings $s$ and $t$ consisting of lowercase English letters.

You may apply the following three operations to $s$ any number of times; each operation counts as one step:

- Insert: insert one character at any position;
- Delete: delete any one character;
- Replace: change any one character into another character.

Compute the minimum number of steps needed to turn $s$ into $t$, i.e. the **edit distance** between the two strings.

### Input

- The first line contains a non-empty string $s$.
- The second line contains a non-empty string $t$.

The strings contain no spaces and consist only of lowercase English letters.

### Output

A single integer: the minimum number of operations that turn $s$ into $t$.

### Constraints

$1 \le |s|, |t| \le 2000$.

### Sample explanation

Sample 1: $s = \texttt{kitten}$ and $t = \texttt{sitting}$.

An optimal solution uses $3$ steps:

1. `kitten` $\to$ `sitten`: replace `k` with `s`;
2. `sitten` $\to$ `sittin`: replace `e` with `i`;
3. `sittin` $\to$ `sitting`: insert `g` at the end.

So the output is `3`.

### Hint

Let $f_{i,j}$ be the minimum number of steps that turn the first $i$ characters of $s$ into the first $j$ characters of $t$. Then

$$f_{i,j} = \begin{cases} f_{i-1,j-1}, & s_i = t_j \\ 1 + \min(f_{i-1,j},\ f_{i,j-1},\ f_{i-1,j-1}), & s_i \ne t_j \end{cases}$$

where $f_{i-1,j}+1$ deletes $s_i$, $f_{i,j-1}+1$ inserts $t_j$, and $f_{i-1,j-1}+1$ replaces $s_i$ with $t_j$.

The boundaries are $f_{0,j} = j$ and $f_{i,0} = i$, and the answer is $f_{|s|,|t|}$. A rolling array reduces the memory to $O(|t|)$.

# Prefix Counting with a Trie

You are given $n$ non-empty lowercase strings (words) $w_1, w_2, \ldots, w_n$ and $q$ non-empty lowercase strings (queries) $t_1, t_2, \ldots, t_q$.

For every query $t_j$, count how many words have it as a prefix, that is, the number of indices $i$ with

$$|w_i| \ge |t_j| \quad\text{and}\quad w_i[1..|t_j|] = t_j.$$

### Input

- The first line contains one integer $n$.
- The second line contains $n$ space-separated lowercase strings $w_1, \ldots, w_n$.
- The third line contains one integer $q$.
- The fourth line contains $q$ space-separated lowercase strings $t_1, \ldots, t_q$.

### Output

Print one line with $q$ space-separated integers; the $j$-th integer is the number of words having $t_j$ as a prefix.

### Constraints

- $1 \le n, q \le 2 \times 10^5$.
- Every word and every query is non-empty and consists of lowercase English letters `a` to `z` only.
- The sum of the lengths of all words is at most $2 \times 10^5$; the sum of the lengths of all queries is at most $2 \times 10^5$.

### Sample explanation

Sample 1: $n = 4$ with words `a`, `ab`, `abc`, `b`; $q = 3$ with queries `a`, `ab`, `d`.

- Query `a`: `a`, `ab`, `abc` all start with it, so $3$ words;
- query `ab`: `ab` and `abc` start with it, so $2$ words;
- query `d`: no word starts with `d`, so $0$ words.

Hence the output is `3 2 0`.

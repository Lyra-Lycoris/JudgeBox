# Word Ladder

You are given two words `begin` and `end`, plus a list of $n$ words.

In one step you may **change exactly one letter** of the current word, producing a new word. The new word must appear in the given list (`begin` itself does not have to be in the list, but `end` does). Each word of the list may be used at most once.

Find the number of words in the shortest "ladder" from `begin` to `end` (both `begin` and `end` are counted). If no such ladder exists, return $0$.

All words consist of lowercase English letters only and share the same length $L$. If `begin` equals `end`, the ladder consists of a single word and the answer is $1$.

### Input

- The first line contains three parts: the integer $n$, the word `begin` and the word `end`, separated by single spaces.
- The second line contains $n$ words separated by single spaces: the word list.

### Output

Print one integer: the number of words in the shortest ladder, or `0` if no ladder exists.

### Constraints

- $1 \le n \le 5000$
- $1 \le L \le 10$
- `begin`, `end` and every listed word have length exactly $L$ and contain lowercase English letters only
- The list may contain duplicates, and may contain `begin` or `end`
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
6 hit cog
hot dot dog lot log cog
```

**Output**

```
5
```

### Sample explanation

A shortest ladder is `hit` → `hot` → `dot` → `dog` → `cog`, which contains $5$ words; each step changes exactly one letter and every intermediate word is in the list.

Since `hit` and `cog` differ in all three positions, at least $3$ steps ($4$ words) are needed, and no $4$-word ladder exists. The answer is therefore `5`.

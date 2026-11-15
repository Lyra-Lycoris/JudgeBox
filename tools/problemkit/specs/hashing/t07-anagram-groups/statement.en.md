# Number of Anagram Groups

Two strings are called **anagrams** if one can be rearranged into the other, i.e. they consist of exactly the same letters with the same multiplicities. For example `listen`, `silent`, `enlist` and `inlets` are pairwise anagrams.

Given $n$ lowercase strings, put strings that are anagrams of each other into the same group (a string is an anagram of itself). Print the number of **distinct groups**, that is, how many different letter multisets occur among the $n$ strings.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ strings, separated by single spaces.

### Output

Print one integer: the number of distinct groups.

### Constraints

$1 \le n \le 200000$, each string has length between $1$ and $10$, and contains only lowercase letters `a` to `z`.

### Sample explanation

Sample 1 contains $6$ strings:

- `listen`, `silent`, `enlist` and `inlets` all have the letter multiset $\{e, i, l, n, s, t\}$, forming group 1;
- `google` and `gogole` both have the multiset $\{e, g, g, l, o, o\}$, forming group 2.

Hence there are $2$ groups and the answer is `2`.

class _TrieNode:
    __slots__ = ("children", "word_id")

    def __init__(self) -> None:
        self.children: dict[str, "_TrieNode"] = {}
        self.word_id = -1


def _build_trie(dictionary: list[str], length: int) -> tuple["_TrieNode", list[str]]:
    root = _TrieNode()
    words: list[str] = []
    for word in dictionary:
        # 词表里可能有空词；忽略空词，保证每条边都向前推进。
        if not word or len(word) > length:
            continue
        node = root
        for letter in word:
            child = node.children.get(letter)
            if child is None:
                child = _TrieNode()
                node.children[letter] = child
            node = child
        if node.word_id < 0:
            node.word_id = len(words)
            words.append(word)
    return root, words


def _build_edges(root: "_TrieNode", text: list[str]) -> list[list[tuple[int, int]]]:
    n = len(text)
    edges: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
    reachable = [False] * (n + 1)
    reachable[n] = True
    for start in range(n - 1, -1, -1):
        node = root
        for end in range(start, n):
            node = node.children.get(text[end])
            if node is None:
                break
            if node.word_id >= 0 and reachable[end + 1]:
                edges[start].append((end + 1, node.word_id))
                reachable[start] = True
    # 按词表首次出现的顺序枚举同一位置上的匹配，答案顺序与标准答案一致。
    for matches in edges:
        matches.sort(key=lambda match: match[1])
    return edges


def _build_word_bits(edges: list[list[tuple[int, int]]], word_count: int) -> list[int]:
    occurrences = [0] * word_count
    for matches in edges:
        for _, word_id in matches:
            occurrences[word_id] += 1
    bits = [0] * word_count
    bit_index = 0
    for word_id in range(word_count):
        # 只出现一次的词不可能复用，无需占据集合状态的一位。
        if occurrences[word_id] > 1:
            bits[word_id] = 1 << bit_index
            bit_index += 1
    return bits


def _build_future_bits(edges: list[list[tuple[int, int]]], word_bits: list[int]) -> list[int]:
    future = [0] * len(edges)
    for index in range(len(edges) - 2, -1, -1):
        mask = future[index + 1]
        for _, word_id in edges[index]:
            mask |= word_bits[word_id]
        future[index] = mask
    return future


class _VerseSolver:
    def __init__(self, verse: str, dictionary: list[str]) -> None:
        text = list(verse)
        root, words = _build_trie(dictionary, len(text))
        self.length = len(text)
        self.words = words
        self.edges = _build_edges(root, text)
        self.word_bits = _build_word_bits(self.edges, len(words))
        self.future_bits = _build_future_bits(self.edges, self.word_bits)
        self.memo: list[dict[int, int]] = [{} for _ in range(self.length + 1)]
        self.path = [""] * self.length
        self.answers: list[str] = []

    def run(self) -> list[str]:
        if not self.edges[0]:
            return []
        self._collect(0, 0, 0)
        return self.answers

    # used 只记录“以前用过、以后仍可能出现”的词；返回后缀最少还需引入的词数。
    def _minimum_cost(self, index: int, used: int) -> int:
        if index == self.length:
            return 0
        memo = self.memo[index]
        cached = memo.get(used)
        if cached is not None:
            return cached
        best = self.length + 1
        edges = self.edges
        word_bits = self.word_bits
        future_bits = self.future_bits
        for end, word_id in edges[index]:
            bit = word_bits[word_id]
            extra = 0 if (used & bit) else 1
            # 越过某个词的最后匹配位置后，该词可以安全地从状态中遗忘。
            cost = extra + self._minimum_cost(end, (used | bit) & future_bits[end])
            if cost < best:
                best = cost
                if best == 0:
                    break
        memo[used] = best
        return best

    def _collect(self, index: int, used: int, depth: int) -> None:
        if index == self.length:
            self.answers.append(" ".join(self.path[:depth]))
            return
        best = self._minimum_cost(index, used)
        edges = self.edges
        word_bits = self.word_bits
        future_bits = self.future_bits
        words = self.words
        path = self.path
        for end, word_id in edges[index]:
            bit = word_bits[word_id]
            extra = 0 if (used & bit) else 1
            next_used = (used | bit) & future_bits[end]
            if extra + self._minimum_cost(end, next_used) == best:
                path[depth] = words[word_id]
                self._collect(end, next_used, depth + 1)


def solve(verse: str, words: list[str]) -> list[str]:
    if not verse:
        return []
    return _VerseSolver(verse, words).run()

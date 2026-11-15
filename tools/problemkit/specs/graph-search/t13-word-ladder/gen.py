import random


def _case(begin, end, words):
    return "%d %s %s\n%s\n" % (len(words), begin, end, " ".join(words))


def _chain(count, width):
    """构造一条相邻单词恰好只差一个字母、且单词互不相同的长链。"""
    chars = ["a"] * width
    words = ["".join(chars)]
    for step in range(1, count):
        pos = step % width
        chars[pos] = chr(97 + 1 + step // width)
        words.append("".join(chars))
    return words


def _unique(rng, alphabet, width, count, seen):
    words = []
    while len(words) < count:
        word = "".join(rng.choice(alphabet) for _ in range(width))
        if word in seen:
            continue
        seen.add(word)
        words.append(word)
    return words


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "6 hit cog\nhot dot dog lot log cog\n"},
        {"id": "02", "input": "2 abc abc\nabd xyz\n"},
        {"id": "03", "input": "2 abc xyz\nabd abe\n"},
        {"id": "04", "input": "3 abc xyz\nabd xyq xyz\n"},
        {"id": "05", "input": "1 abc abd\nabd\n"},
        {"id": "06", "input": "3 a m\nb n m\n"},
    ]

    def add(text):
        out.append({"id": "%02d" % (len(out) + 1), "input": text})

    chain = _chain(251, 10)
    add(_case(chain[0], chain[-1], chain))

    seen = set()
    pool = _unique(rng, "abcdefgh", 5, 5000, seen)
    add(_case(pool[0], pool[2500], pool))

    left = _unique(rng, "abcde", 5, 2500, seen)
    right = _unique(rng, "vwxyz", 5, 2500, seen)
    add(_case(left[0], right[0], left + right))

    words = []
    for a in "abc":
        for b in "abc":
            for c in "abc":
                words.append(a + b + c)
    rng.shuffle(words)
    words = words[:20]
    add(_case(words[0], words[10], words))

    add(_case("aaaaaaaaaa", "aaaaaaaaab", ["aaaaaaaaaa", "aaaaaaaaab", "zzzzzzzzzz"]))

    add(_case(chain[100], chain[100], chain))
    return out

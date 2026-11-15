import itertools
import random


def _hints(secret, guess):
    n = len(secret)
    a = 0
    ca = [0] * 10
    cb = [0] * 10
    for i in range(n):
        if secret[i] == guess[i]:
            a += 1
        ca[secret[i]] += 1
        cb[guess[i]] += 1
    b = sum(min(ca[d], cb[d]) for d in range(10)) - a
    return a, b


def _format_case(n, pairs):
    guesses = " ".join("".join(str(d) for d in g) for g, _ in pairs)
    exact = " ".join(str(h[0]) for _, h in pairs)
    loose = " ".join(str(h[1]) for _, h in pairs)
    return "%d %d\n%s\n%s\n%s\n" % (n, len(pairs), guesses, exact, loose)


def _fixed(n, secret, guesses):
    pairs = [(g, _hints(secret, g)) for g in guesses]
    _verify(n, secret, pairs)
    return _format_case(n, pairs)


def _random_case(n, secret, rng, min_k, max_k):
    cands = list(itertools.product(range(10), repeat=n))
    pairs, used = [], set()

    def add(guess):
        nonlocal cands
        h = _hints(secret, guess)
        pairs.append((guess, h))
        used.add(guess)
        cands = [c for c in cands if _hints(c, guess) == h]

    guard = 0
    while len(cands) > 1 and len(pairs) < max_k and guard < 500:
        guard += 1
        g = tuple(rng.randrange(10) for _ in range(n))
        if g == secret or g in used:
            continue
        add(g)
    guard = 0
    while len(pairs) < min_k and guard < 500:
        guard += 1
        g = tuple(rng.randrange(10) for _ in range(n))
        if g == secret or g in used:
            continue
        add(g)
    if len(cands) != 1:
        add(secret)
    _verify(n, secret, pairs)
    return _format_case(n, pairs)


def _verify(n, secret, pairs):
    cands = [c for c in itertools.product(range(10), repeat=n)
             if all(_hints(c, g) == h for g, h in pairs)]
    assert len(cands) == 1 and cands[0] == secret, (n, secret, pairs[:3], len(cands))


def cases():
    rng = random.Random(20261118)
    out = []

    # 01 样例：n = 3，三条提示唯一确定 427
    out.append({"id": "01", "input": _fixed(3, (4, 2, 7), [(1, 2, 3), (7, 2, 0), (2, 4, 7)])})

    # 02 边界 n = 1，猜中
    out.append({"id": "02", "input": _fixed(1, (0,), [(0,)])})

    # 03 边界 n = 1，把 10 个数字各猜一遍
    out.append({"id": "03", "input": _fixed(1, (5,), [(d,) for d in range(10)])})

    # 04 n = 2，密码有前导零
    out.append({"id": "04", "input": _fixed(2, (0, 7), [(7, 0)])})

    # 05 四位全相同
    out.append({"id": "05", "input": _random_case(4, (7, 7, 7, 7), rng, 6, 12)})

    # 06 四位互不相同且带前导零
    out.append({"id": "06", "input": _random_case(4, (0, 1, 2, 3), rng, 8, 16)})

    # 07 三位的随机密码
    out.append({"id": "07", "input": _random_case(3, (5, 2, 8), rng, 3, 8)})

    # 08 提示很多（k = 20）
    out.append({"id": "08", "input": _random_case(4, (5, 0, 5, 0), rng, 20, 24)})

    # 09 密码全为 0
    out.append({"id": "09", "input": _random_case(4, (0, 0, 0, 0), rng, 6, 12)})

    # 10 四位互不相同
    out.append({"id": "10", "input": _random_case(4, (1, 2, 3, 4), rng, 10, 16)})

    return out

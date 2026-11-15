def solve(n: int, words: list[str], q: int, queries: list[str]) -> list[int]:
    children = [{}]
    passing = [0]
    for word in words:
        current = 0
        for ch in word:
            nxt = children[current].get(ch)
            if nxt is None:
                nxt = len(children)
                children[current][ch] = nxt
                children.append({})
                passing.append(0)
            current = nxt
            passing[current] += 1
    answer = []
    for query in queries:
        current = 0
        found = True
        for ch in query:
            nxt = children[current].get(ch)
            if nxt is None:
                found = False
                break
            current = nxt
        answer.append(passing[current] if found else 0)
    return answer

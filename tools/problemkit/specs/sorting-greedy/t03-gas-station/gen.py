import random


def pack(gas, cost):
    return "%d\n%s\n%s\n" % (len(gas), " ".join(str(x) for x in gas),
                             " ".join(str(x) for x in cost))


def cases():
    rng = random.Random(20260303)
    out = [{"id": "01", "input": pack([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])}]
    out.append({"id": "02", "input": pack([1], [2])})
    out.append({"id": "03", "input": pack([2], [1])})
    out.append({"id": "04", "input": pack([0, 0, 0, 0], [0, 0, 0, 0])})
    out.append({"id": "05", "input": pack([0, 1], [1, 0])})
    out.append({"id": "06", "input": pack([0, 0, 5], [10, 10, 0])})

    n = 2000
    cost = [rng.randint(0, 5000) for _ in range(n)]
    gas = [cost[i] + rng.randint(0, 10) for i in range(n)]
    out.append({"id": "07", "input": pack(gas, cost)})

    n = 100000
    cost = [rng.randint(0, 5000) for _ in range(n)]
    gas = [cost[i] + rng.randint(0, 10) for i in range(n)]
    out.append({"id": "08", "input": pack(gas, cost)})

    n = 100000
    gas = [rng.randint(0, 10000) for _ in range(n)]
    cost = [rng.randint(0, 10000) for _ in range(n)]
    out.append({"id": "09", "input": pack(gas, cost)})
    return out

import random


def pack(cases_list):
    lines = [str(len(cases_list))]
    for a in cases_list:
        lines.append(str(len(a)))
        lines.append(" ".join(str(x) for x in a))
    return "\n".join(lines) + "\n"


def cases():
    rng = random.Random(20260904)
    out = [{"id": "01", "input": pack([[1, 2, 3], [5, 4, 3, 2]])}]
    out.append({"id": "02", "input": pack([[-7]])})
    out.append({"id": "03", "input": pack([[5, 5, 5, 5, 5]])})
    out.append({"id": "04", "input": pack([[-1, -2, -3, -4]])})
    out.append({"id": "05", "input": pack([[-1000000000, 1000000000]])})
    out.append({"id": "06", "input": pack([[1], [2, 1], [3, 2, 1], [9, 8, 7, 6, 5], [0, 0]])})
    out.append({"id": "07", "input": pack([[rng.randint(-10 ** 9, 10 ** 9) for _ in range(2000)]])})
    out.append({"id": "08", "input": pack([[rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)],
                                           [rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)]])})
    out.append({"id": "09", "input": pack([list(range(1, 200001))])})
    return out

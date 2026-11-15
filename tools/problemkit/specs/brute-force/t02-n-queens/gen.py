def cases():
    out = []

    # 01 样例：4 皇后有 2 种方案
    out.append({"id": "01", "input": "4\n"})

    # 02..10 覆盖 n = 1 .. 10
    for n in (1, 2, 3, 5, 6, 7, 8, 9, 10):
        out.append({"id": "%02d" % (len(out) + 1), "input": "%d\n" % n})

    return out

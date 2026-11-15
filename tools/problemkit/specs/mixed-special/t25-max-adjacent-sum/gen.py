def cases():
    out = [{"id": "01", "input": "5\n"}]
    for n in (1, 2, 3, 4, 6, 7, 8):
        out.append({"id": "%02d" % (len(out) + 1), "input": "%d\n" % n})
    for n in (1000, 99999, 200000, 199999):
        out.append({"id": "%02d" % (len(out) + 1), "input": "%d\n" % n})
    return out

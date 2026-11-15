def cases():
    out = []

    # 01 样例：123, 132, 213 -> 第 3 个是 2 1 3
    out.append({"id": "01", "input": "3 3\n"})

    # 02 边界 n = 1
    out.append({"id": "02", "input": "1 1\n"})

    # 03 边界 n = 2
    out.append({"id": "03", "input": "2 2\n"})

    # 04 最大 n，第一个排列
    out.append({"id": "04", "input": "9 1\n"})

    # 05 最大 n，最后一个排列（9! = 362880）
    out.append({"id": "05", "input": "9 362880\n"})

    # 06 最大 n，正中间的排列
    out.append({"id": "06", "input": "9 181440\n"})

    # 07 n = 8 的最后一个排列（8! = 40320）
    out.append({"id": "07", "input": "8 40320\n"})

    # 08 最大 n 的随机名次
    out.append({"id": "08", "input": "9 123456\n"})

    # 09 小规模随机名次
    out.append({"id": "09", "input": "5 100\n"})

    # 10 n = 7 的最后一个排列（7! = 720）
    out.append({"id": "10", "input": "7 720\n"})

    # 11 最大 n 的另一个随机名次
    out.append({"id": "11", "input": "9 200000\n"})

    return out

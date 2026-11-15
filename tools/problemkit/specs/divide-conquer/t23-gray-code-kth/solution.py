def solve(n: int, k: int) -> int:
    def gray(bits: int, index: int) -> int:
        if bits == 0:
            return 0
        half = 1 << (bits - 1)
        if index < half:
            return gray(bits - 1, index)
        return half + gray(bits - 1, 2 * half - 1 - index)

    return gray(n, k)

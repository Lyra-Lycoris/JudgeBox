# driver：追加在选手代码后面，只负责读 stdin、调用 solve、写 stdout。
# 约定：函数式提交时选手代码在前、这里的内容在后，所以 main() 调用写在最后。
import sys


def main():
    data = sys.stdin.buffer.read().split()
    a = int(data[0])
    b = int(data[1])
    print(solve(a, b))


main()

// SPJ：自己读输入、自己判断选手输出，不依赖 .ans。
// 平台会以 `checker.exe <input> <output> <answer>` 调用；需要标准输出比对的题可以删掉这个文件，
// 平台会退回「逐行 token 比较」。
#include "testlib.h"

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long a = inf.readLong();
    long long b = inf.readLong();
    long long expected = a + b;

    long long actual = ouf.readLong();
    if (actual != expected) quitf(_wa, "期望 %lld，实际 %lld", expected, actual);

    // quit 时 testlib 会自动检查输出文件是否还有多余内容（多于的空白不算）。
    quitf(_ok, "ok");
}

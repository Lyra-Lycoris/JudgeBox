// SPJ：选手只需输出任意一个长度为 n、最大嵌套深度为 k 的合法括号序列。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <string>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();
    long long k = inf.readLong();

    std::string s = ouf.readToken();
    if (!ouf.seekEof()) quitf(_wa, "输出多余的内容（应只有一个长度为 %lld 的括号序列）", n);

    if ((long long)s.size() != n) quitf(_wa, "括号序列长度为 %d，应为 %lld", (int)s.size(), n);

    long long balance = 0, depth = 0;
    for (int i = 0; i < n; ++i) {
        char ch = s[i];
        if (ch == '(') {
            ++balance;
        } else if (ch == ')') {
            --balance;
        } else {
            quitf(_wa, "第 %d 个字符不是括号", i + 1);
        }
        if (balance < 0) quitf(_wa, "第 %d 个字符处右括号过多，前缀不合法", i + 1);
        if (balance > depth) depth = balance;
    }
    if (balance != 0) quitf(_wa, "左括号比右括号多 %lld 个", balance);
    if (depth != k) quitf(_wa, "最大嵌套深度为 %lld，应为 %lld", depth, k);

    quitf(_ok, "ok");
}

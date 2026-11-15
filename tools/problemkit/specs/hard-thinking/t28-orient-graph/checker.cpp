// SPJ：选手输出任意一个合法定向即可（每条边 a_i -> b_i，每个点入度 <= 1），无解时输出 -1。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

static int orientFind(std::vector<int>& parent, int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();
    long long m = inf.readLong();
    if (n < 1 || n > 200000) quitf(_fail, "输入不合法：n = %lld", n);
    if (m < 0 || m > 200000) quitf(_fail, "输入不合法：m = %lld", m);

    std::vector<long long> eu((size_t)m), ev((size_t)m);
    std::vector<int> parent((size_t)n + 1), vertCnt((size_t)n + 1, 0), edgeCnt((size_t)n + 1, 0);
    for (int i = 0; i <= (int)n; ++i) parent[(size_t)i] = i;
    for (long long i = 0; i < m; ++i) {
        long long a = inf.readLong(1LL, n);
        long long b = inf.readLong(1LL, n);
        if (a == b) quitf(_fail, "输入不合法：第 %lld 条边是自环", i + 1);
        eu[(size_t)i] = a;
        ev[(size_t)i] = b;
        int ra = orientFind(parent, (int)a);
        int rb = orientFind(parent, (int)b);
        if (ra != rb) parent[(size_t)ra] = rb;
    }
    for (long long i = 0; i < m; ++i) ++edgeCnt[(size_t)orientFind(parent, (int)eu[(size_t)i])];
    for (long long v = 1; v <= n; ++v) ++vertCnt[(size_t)orientFind(parent, (int)v)];
    bool feasible = true;
    for (long long v = 1; v <= n; ++v) {
        if (orientFind(parent, (int)v) == (int)v && edgeCnt[(size_t)v] > vertCnt[(size_t)v]) {
            feasible = false;
        }
    }

    std::vector<long long> out;
    while (!ouf.seekEof()) {
        out.push_back(ouf.readLong());
    }

    if (!feasible) {
        if (out.size() == 1 && out[0] == -1) quitf(_ok, "ok：图不可定向");
        quitf(_wa, "该图不存在合法定向，应当只输出一个 -1");
    }
    if (out.size() == 1 && out[0] == -1) {
        quitf(_wa, "该图存在合法定向，但输出为 -1");
    }
    if ((long long)out.size() != 2 * m) {
        quitf(_wa, "输出个数不对：期望 %lld 个整数，实际 %d 个", 2 * m, (int)out.size());
    }

    std::vector<long long> indeg((size_t)n + 1, 0);
    for (long long i = 0; i < m; ++i) {
        long long a = out[(size_t)(2 * i)];
        long long b = out[(size_t)(2 * i + 1)];
        long long u = eu[(size_t)i], v = ev[(size_t)i];
        if (!((a == u && b == v) || (a == v && b == u))) {
            quitf(_wa, "第 %lld 条边 (%lld,%lld) 的方向 (%lld,%lld) 不合法", i + 1, u, v, a, b);
        }
        ++indeg[(size_t)b];
    }
    for (long long v = 1; v <= n; ++v) {
        if (indeg[(size_t)v] > 1) {
            quitf(_wa, "点 %lld 的入度为 %lld，超过了 1", v, indeg[(size_t)v]);
        }
    }

    quitf(_ok, "ok");
}

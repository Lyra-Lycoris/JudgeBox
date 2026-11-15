// driver：平台会补上 import 与 class Main 外壳，这里只写类体。
// 只负责读 stdin、调用选手的 solve、写 stdout。
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long a = Long.parseLong(br.readLine().trim());
        long b = Long.parseLong(br.readLine().trim());
        System.out.println(solve(a, b));
    }

def solve():
    parts = input().split()
    cr, ci, cd = int(parts[0]), int(parts[1]), int(parts[2])
    cd2 = int(parts[3]) if len(parts) > 3 else 10**9
    a = input().strip()
    b = input().strip()
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i * cd
    for j in range(1, m + 1):
        dp[0][j] = j * ci
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            best = dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else cr)
            v = dp[i - 1][j] + cd
            if v < best:
                best = v
            v = dp[i][j - 1] + ci
            if v < best:
                best = v
            if i >= 2 and j > 0 and b[j - 1] == a[i - 2]:
                v = dp[i - 2][j] + cd2
                if v < best:
                    best = v
            dp[i][j] = best
    print(dp[n][m])

solve()
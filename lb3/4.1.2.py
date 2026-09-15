def solve():
    parts = input().split()
    cr, ci, cd = int(parts[0]), int(parts[1]), int(parts[2])
    cd2 = int(parts[3]) if len(parts) > 3 else 10**9
    a = input().strip()
    b = input().strip()
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    op = [[''] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i * cd
        op[i][0] = 'D'
    for j in range(1, m + 1):
        dp[0][j] = j * ci
        op[0][j] = 'I'
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            best = dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else cr)
            best_op = 'M' if a[i - 1] == b[j - 1] else 'R'
            v = dp[i - 1][j] + cd
            if v < best:
                best = v
                best_op = 'D'
            v = dp[i][j - 1] + ci
            if v < best:
                best = v
                best_op = 'I'
            if i >= 2 and j > 0 and b[j - 1] == a[i - 2]:
                v = dp[i - 2][j] + cd2
                if v < best:
                    best = v
                    best_op = 'D2'
            dp[i][j] = best
            op[i][j] = best_op
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        o = op[i][j]
        if o == 'M' or o == 'R':
            ops.append(o)
            i -= 1
            j -= 1
        elif o == 'D':
            ops.append('D')
            i -= 1
        elif o == 'I':
            ops.append('I')
            j -= 1
        elif o == 'D2':
            ops.append('D')
            ops.append('D')
            i -= 2
    ops.reverse()
    print(''.join(ops))
    print(a)
    print(b)

solve()
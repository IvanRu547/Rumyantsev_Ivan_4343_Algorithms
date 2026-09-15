def solve():
    parts = input().split()
    cr, ci, cd, cd2 = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
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
            cost_match = 0 if a[i - 1] == b[j - 1] else cr
            best = dp[i - 1][j - 1] + cost_match
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

    print("=== Таблица DP (стоимости) ===")
    header = ["    "] + ["  " + c for c in [" "] + list(b)]
    print("".join(header))
    print("    " + "-" * (4 * (m + 1)))
    print("  ." + "".join(f"{dp[0][j]:4d}" for j in range(m + 1)))
    for i in range(1, n + 1):
        row_str = f" {a[i-1]}." + "".join(f"{dp[i][j]:4d}" for j in range(m + 1))
        print(row_str)

    print("\n=== Таблица операций ===")
    header = ["    "] + ["  " + c for c in [" "] + list(b)]
    print("".join(header))
    print("    " + "-" * (4 * (m + 1)))
    print("  ." + "".join(f"{op[0][j]:>4}" for j in range(m + 1)))
    for i in range(1, n + 1):
        row_str = f" {a[i-1]}." + "".join(f"{op[i][j]:>4}" for j in range(m + 1))
        print(row_str)

    ops = []
    i, j = n, m
    print("\n=== Восстановление предписания ===")
    while i > 0 or j > 0:
        o = op[i][j]
        if o == 'M':
            print(f"  [{i},{j}] M: символы '{a[i-1]}' и '{b[j-1]}' совпадают -> переход в [{i-1},{j-1}]")
            ops.append('M')
            i -= 1
            j -= 1
        elif o == 'R':
            print(f"  [{i},{j}] R: замена '{a[i-1]}' на '{b[j-1]}' (цена {cr}) -> переход в [{i-1},{j-1}]")
            ops.append('R')
            i -= 1
            j -= 1
        elif o == 'D':
            print(f"  [{i},{j}] D: удаление '{a[i-1]}' (цена {cd}) -> переход в [{i-1},{j}]")
            ops.append('D')
            i -= 1
        elif o == 'I':
            print(f"  [{i},{j}] I: вставка '{b[j-1]}' (цена {ci}) -> переход в [{i},{j-1}]")
            ops.append('I')
            j -= 1
        elif o == 'D2':
            print(f"  [{i},{j}] D2: удаление пары '{a[i-2]}{a[i-1]}' (цена {cd2}), проверка: b[{j-1}]='{b[j-1]}' == a[{i-2}]='{a[i-2]}' -> переход в [{i-2},{j}]")
            ops.append('D')
            ops.append('D')
            i -= 2
    ops.reverse()

    print("\n=== Результат ===")
    print("Предписание:", ''.join(ops))
    print("Исходная строка A:", a)
    print("Целевая строка B: ", b)
    print("Минимальная стоимость:", dp[n][m])

solve()
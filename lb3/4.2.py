def solve():
    a = input().strip()
    b = input().strip()
    if len(a) < len(b):
        a, b = b, a
    n, m = len(a), len(b)
    
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    for i in range(n):
        curr[0] = i + 1
        ai = a[i]
        for j in range(m):
            if ai == b[j]:
                curr[j + 1] = prev[j]
            else:
                v1 = prev[j]
                v2 = prev[j + 1]
                v3 = curr[j]
                if v2 < v1:
                    v1 = v2
                if v3 < v1:
                    v1 = v3
                curr[j + 1] = v1 + 1
        prev, curr = curr, prev
    
    print(prev[m])

solve()
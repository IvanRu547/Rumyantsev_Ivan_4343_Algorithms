def kmp_search(P, T):
    
    n, m = len(T), len(P)
    
   
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and P[i] != P[j]:
            j = pi[j - 1]
        if P[i] == P[j]:
            j += 1
        pi[i] = j
    

    matches = []
    j = 0  
    
    for i in range(n):
        while j > 0 and T[i] != P[j]:
            j = pi[j - 1]
        if T[i] == P[j]:
            j += 1
        if j == m:
         
            matches.append(i - m + 1)
            j = pi[j - 1]
    
    return matches


P = input().strip()
T = input().strip()


result = kmp_search(P, T)


if result:
    print(",".join(map(str, result)))
else:
    print("-1")
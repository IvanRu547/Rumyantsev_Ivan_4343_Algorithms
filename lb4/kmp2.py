import sys

def kmp_first_occurrence(P, T):
    """Находит первое вхождение P в T. Возвращает индекс или -1."""
    n, m = len(T), len(P)
    if m == 0:
        return 0
    if n < m:
        return -1

    # Префикс-функция для P
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and P[i] != P[j]:
            j = pi[j - 1]
        if P[i] == P[j]:
            j += 1
        pi[i] = j

    # Поиск первого вхождения
    j = 0
    for i in range(n):
        while j > 0 and T[i] != P[j]:
            j = pi[j - 1]
        if T[i] == P[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

# Чтение входных данных (быстрый ввод для строк до 5 млн)
A = sys.stdin.readline().rstrip('\n')
B = sys.stdin.readline().rstrip('\n')

if len(A) != len(B):
    print(-1)
elif len(A) == 0:
    print(0)
else:
    # Ищем B в A+A
    idx = kmp_first_occurrence(B, A + A)
    if idx != -1 and idx < len(A):
        print(idx)
    else:
        print(-1)
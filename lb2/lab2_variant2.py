import sys
import heapq
import random
import os

DEBUG = True

def debug(*args):
    if DEBUG:
        print(*args)

INF = float('inf')


def generate_matrix(n, symmetric=True, max_weight=50.0,
                    allow_missing=False, missing_prob=0.1):
    mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if allow_missing and random.random() < missing_prob:
                w = INF
            else:
                w = round(random.uniform(1, max_weight), 2)
            mat[i][j] = w
            if symmetric:
                mat[j][i] = w
            else:
                if allow_missing and random.random() < missing_prob:
                    mat[j][i] = INF
                else:
                    mat[j][i] = round(random.uniform(1, max_weight), 2)
    return mat


def save_matrix(mat, filename):
    n = len(mat)
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            row = []
            for j in range(n):
                if i == j or mat[i][j] == INF:
                    row.append("-1")
                else:
                    row.append(f"{mat[i][j]:.2f}")
            f.write(" ".join(row) + "\n")
    debug(f"[FILE] Матрица сохранена в {filename}")


def load_matrix(filename):
    with open(filename, 'r') as f:
        data = f.read().split()
    it = iter(data)
    n = int(next(it))
    mat = []
    for i in range(n):
        row = []
        for j in range(n):
            v = float(next(it))
            if v == -1.0 or i == j:
                row.append(INF)
            else:
                row.append(v)
        mat.append(row)
    debug(f"[FILE] Матрица загружена из {filename}, размер {n}x{n}")
    return mat


def matrix_from_list(lst):
    n = len(lst)
    mat = []
    for i in range(n):
        row = []
        for j in range(n):
            v = lst[i][j]
            if v == -1 or i == j:
                row.append(INF)
            else:
                row.append(float(v))
        mat.append(row)
    return mat


def nearest_neighbor(adj, start=0):
    n = len(adj)
    visited = [False] * n
    visited[start] = True
    path = [start]
    curr = start
    cost = 0.0

    debug(f"\n[АБС] Старт из вершины {start}")
    for step in range(n - 1):
        best_w = INF
        best_v = -1
        for v in range(n):
            if not visited[v] and adj[curr][v] < best_w:
                best_w = adj[curr][v]
                best_v = v
        if best_v == -1 or best_w == INF:
            debug("[АБС] Нет допустимого перехода — маршрут не найден")
            return None, INF
        debug(f"[АБС] Шаг {step+1}: {curr} -> {best_v} (вес {best_w:.2f})")
        visited[best_v] = True
        path.append(best_v)
        cost += best_w
        curr = best_v

    if adj[curr][start] == INF:
        debug("[АБС] Нет обратного ребра в старт — маршрут не найден")
        return None, INF
    cost += adj[curr][start]
    debug(f"[АБС] Возврат {curr} -> {start} (вес {adj[curr][start]:.2f})")
    debug(f"[АБС] Итог: путь {path}, стоимость {cost:.2f}")
    return path, cost


def half_sum_lower_bound(pieces, adj):
    m = len(pieces)
    if m <= 1:
        return 0.0
    total = 0.0
    cnt = 0
    for piece in pieces:
        start_v = piece[0]
        end_v = piece[-1]
        mn_in = INF
        for other in pieces:
            if other is piece:
                continue
            u = other[-1]
            if adj[u][start_v] < mn_in:
                mn_in = adj[u][start_v]
        mn_out = INF
        for other in pieces:
            if other is piece:
                continue
            v = other[0]
            if adj[end_v][v] < mn_out:
                mn_out = adj[end_v][v]
        if mn_in != INF:
            total += mn_in
            cnt += 1
        if mn_out != INF:
            total += mn_out
            cnt += 1
    if cnt == 0:
        return INF
    return total / 2.0


def mst_lower_bound(pieces, adj):
    m = len(pieces)
    if m <= 1:
        return 0.0
    edges = []
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            u = pieces[i][-1]
            v = pieces[j][0]
            w = adj[u][v]
            if w != INF:
                edges.append((w, i, j))
    if not edges:
        return INF
    parent = list(range(m))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[rb] = ra
        return True
    edges.sort()
    total = 0.0
    cnt = 0
    for w, i, j in edges:
        if union(i, j):
            total += w
            cnt += 1
            if cnt == m - 1:
                break
    if cnt != m - 1:
        return INF
    return total


def lower_bound(pieces, adj, reduction):
    hs = half_sum_lower_bound(pieces, adj)
    mst = mst_lower_bound(pieces, adj)
    extra = max(reduction, hs, mst)
    debug(f"    [LB] приведение={reduction:.2f}, полусумма={hs:.2f}, "
          f"МОД={mst:.2f}, max={extra:.2f}")
    return extra


def little_with_mst(adj, start=0):
    n = len(adj)
    if n == 1:
        return [0], 0.0
    if n == 2:
        if adj[0][1] != INF and adj[1][0] != INF:
            return [0, 1], adj[0][1] + adj[1][0]
        return None, INF

    def reduce_matrix(mat):
        m = [row[:] for row in mat]
        reduction = 0.0
        for i in range(n):
            mn = INF
            for j in range(n):
                if m[i][j] < mn:
                    mn = m[i][j]
            if mn != INF and mn > 0:
                reduction += mn
                for j in range(n):
                    if m[i][j] != INF:
                        m[i][j] -= mn
        for j in range(n):
            mn = INF
            for i in range(n):
                if m[i][j] < mn:
                    mn = m[i][j]
            if mn != INF and mn > 0:
                reduction += mn
                for i in range(n):
                    if m[i][j] != INF:
                        m[i][j] -= mn
        return reduction, m

    def find_best_edge(mat, succ, pred):
        best_penalty = -1
        best_edge = None
        for i in range(n):
            for j in range(n):
                if mat[i][j] != 0:
                    continue
                si = i
                while pred[si] != -1:
                    si = pred[si]
                sj = j
                while pred[sj] != -1:
                    sj = pred[sj]
                if si == sj:
                    continue
                row_min = INF
                for k in range(n):
                    if k != j and mat[i][k] < row_min:
                        row_min = mat[i][k]
                col_min = INF
                for k in range(n):
                    if k != i and mat[k][j] < col_min:
                        col_min = mat[k][j]
                if row_min == INF: row_min = 0
                if col_min == INF: col_min = 0
                penalty = row_min + col_min
                if penalty > best_penalty:
                    best_penalty = penalty
                    best_edge = (i, j)
        return best_edge

    pieces = [[start]] + [[i] for i in range(n) if i != start]

    init_red, init_mat = reduce_matrix(adj)
    debug(f"\n[ЛИТТЛ] Старт из вершины {start}")
    debug(f"[ЛИТТЛ] Начальное приведение = {init_red:.2f}")

    counter = 0
    pq = []
    init_succ = [-1] * n
    init_pred = [-1] * n
    extra = lower_bound(pieces, adj, init_red)
    heapq.heappush(pq, (extra, counter, init_mat, pieces, 0.0,
                        init_succ, init_pred))

    best_cost = INF
    best_path = None

    while pq:
        lb, _, mat, pieces, cost, succ, pred = heapq.heappop(pq)
        if lb > best_cost + 1e-9:
            continue
        m = len(pieces)
        if m == 1:
            path = pieces[0]
            last = path[-1]
            first = path[0]
            if adj[last][first] != INF:
                total = cost + adj[last][first]
                if total < best_cost - 1e-9:
                    best_cost = total
                    if path[0] != start:
                        idx = path.index(start)
                        path = path[idx:] + path[:idx]
                    best_path = path[:]
                    debug(f"  [ЛИТТЛ] Новый лучший путь: {best_path}, "
                          f"стоимость {best_cost:.2f}")
                elif abs(total - best_cost) <= 1e-9:
                    p = path[:]
                    if p[0] != start:
                        idx = p.index(start)
                        p = p[idx:] + p[:idx]
                    if best_path is None or p < best_path:
                        best_path = p
            continue

        edge = find_best_edge(mat, succ, pred)
        if edge is None:
            continue
        i, j = edge

        start_i = i
        while pred[start_i] != -1:
            start_i = pred[start_i]
        end_j = j
        while succ[end_j] != -1:
            end_j = succ[end_j]

        new_succ = list(succ)
        new_pred = list(pred)
        new_succ[i] = j
        new_pred[j] = i

        new_pieces = []
        pi = pj = -1
        for idx, p in enumerate(pieces):
            if p[-1] == i:
                pi = idx
            if p[0] == j:
                pj = idx
        for idx, p in enumerate(pieces):
            if idx == pi or idx == pj:
                continue
            new_pieces.append(p[:])
        merged = pieces[pi][:] + pieces[pj][:]
        new_pieces.append(merged)

        left_mat = [row[:] for row in mat]
        for k in range(n):
            left_mat[i][k] = INF
            left_mat[k][j] = INF
        if end_j != start_i:
            left_mat[end_j][start_i] = INF
        left_red, left_mat = reduce_matrix(left_mat)
        left_cost = cost + adj[i][j]
        left_lb = lower_bound(new_pieces, adj, left_red) + left_cost

        if left_lb <= best_cost + 1e-9:
            counter += 1
            heapq.heappush(pq, (left_lb, counter, left_mat,
                                new_pieces, left_cost, new_succ, new_pred))

        right_mat = [row[:] for row in mat]
        right_mat[i][j] = INF
        right_red, right_mat = reduce_matrix(right_mat)
        right_lb = lower_bound(pieces, adj, right_red) + cost
        if right_lb <= best_cost + 1e-9:
            counter += 1
            heapq.heappush(pq, (right_lb, counter, right_mat,
                                pieces[:], cost, list(succ), list(pred)))

    return best_path, best_cost


def choose_matrix():
    print("Выберите способ задания матрицы:")
    print("1 — сгенерировать новую")
    print("2 — загрузить из файла")
    choice = input("Ваш выбор (1/2): ").strip()

    if choice == "2":
        filename = input("Имя файла: ").strip()
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден.")
            sys.exit(1)
        adj = load_matrix(filename)
        return adj

    n = int(input("Размер матрицы N: ").strip())
    sym_input = input("Симметричная? (y/n): ").strip().lower()
    symmetric = (sym_input == "y")
    max_w = float(input("Максимальный вес: ").strip())
    adj = generate_matrix(n, symmetric=symmetric, max_weight=max_w)

    save_choice = input("Сохранить матрицу в файл? (y/n): ").strip().lower()
    if save_choice == "y":
        filename = input("Имя файла: ").strip()
        save_matrix(adj, filename)
    return adj


def main():
   

    adj = choose_matrix()
    start = int(input("Стартовая вершина: ").strip())

    nn_path, nn_cost = nearest_neighbor(adj, start)
    little_path, little_cost = little_with_mst(adj, start)

    print("РЕЗУЛЬТАТЫ")

    print(f"АБС:    путь {nn_path}, стоимость {nn_cost:.2f}")
    print(f"Литтл:  путь {little_path}, стоимость {little_cost:.2f}")


if __name__ == "__main__":
    main()
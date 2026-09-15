#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <windows.h>

using namespace std;

bool DEBUG = false;   // true — отладка, false — только ответ

int N;
int M;
int board[20][20];
int empty_area;
int best_count;
vector<pair<pair<int,int>,int>> best_solution;
vector<pair<pair<int,int>,int>> current;

vector<pair<pair<int,int>,int>> required;
vector<bool> required_used;

string indent(int depth) {
    return string(depth * 2, ' ');
}

bool can_place(int x, int y, int side) {
    if (x + side > N || y + side > N) return false;
    for (int i = x; i < x + side; i++)
        for (int j = y; j < y + side; j++)
            if (board[i][j]) return false;
    return true;
}

void set_square(int x, int y, int side, int value) {
    for (int i = x; i < x + side; i++)
        for (int j = y; j < y + side; j++)
            board[i][j] = value;
    if (value) empty_area -= side * side;
    else        empty_area += side * side;
}

bool find_empty(int &x, int &y) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (!board[i][j]) { x = i; y = j; return true; }
    return false;
}

bool conflicts_with_required(int x, int y, int side) {
    for (int idx = 0; idx < M; idx++) {
        if (required_used[idx]) continue;
        int rx = required[idx].first.first;
        int ry = required[idx].first.second;
        int rw = required[idx].second;
        if (rx == x && ry == y && rw == side) continue;
        if (!(x + side <= rx || rx + rw <= x || y + side <= ry || ry + rw <= y)) {
            return true;
        }
    }
    return false;
}

int find_required_idx(int x, int y, int side) {
    for (int idx = 0; idx < M; idx++) {
        if (required[idx].first.first == x &&
            required[idx].first.second == y &&
            required[idx].second == side) {
            return idx;
        }
    }
    return -1;
}

void backtrack(int count, int depth) {
    if (DEBUG) cout << indent(depth) << "backtrack: count=" << count
                    << ", empty=" << empty_area
                    << ", best=" << best_count << "\n";

    if (count >= best_count && empty_area > 0) {
        if (DEBUG) cout << indent(depth) << "  отсечение: count >= best\n";
        return;
    }

    if (empty_area == 0) {
        bool all_used = true;
        for (int idx = 0; idx < M; idx++)
            if (!required_used[idx]) { all_used = false; break; }

        if (!all_used) {
            if (DEBUG) cout << indent(depth) << "  поле заполнено, но не все обязательные\n";
            return;
        }

        if (count < best_count) {
            best_count = count;
            best_solution = current;
            if (DEBUG) cout << indent(depth) << ">>> рекорд: " << count << "\n";
        }
        return;
    }

    int x, y;
    if (!find_empty(x, y)) return;

    if (DEBUG) cout << indent(depth) << "  клетка (" << x+1 << "," << y+1 << ")\n";

    int max_side = min(N - x, N - y);
    if (max_side > N - 1) max_side = N - 1;

    int lb = (empty_area + max_side * max_side - 1) / (max_side * max_side);
    if (count + lb >= best_count) {
        if (DEBUG) cout << indent(depth) << "  отсечение: lb (count=" << count
                        << " + lb=" << lb << " >= best=" << best_count << ")\n";
        return;
    }

    for (int side = max_side; side >= 1; side--) {
        if (!can_place(x, y, side)) continue;
        if (conflicts_with_required(x, y, side)) {
            if (DEBUG) cout << indent(depth) << "  W=" << side << " конфликт с обязательным\n";
            continue;
        }

        int req_idx = find_required_idx(x, y, side);

        if (DEBUG) {
            cout << indent(depth) << "  + " << side << "x" << side
                 << " в (" << x+1 << "," << y+1 << ")";
            if (req_idx != -1) cout << " [обяз #" << req_idx << "]";
            cout << "\n";
        }

        set_square(x, y, side, 1);
        current.push_back({{x, y}, side});
        if (req_idx != -1) required_used[req_idx] = true;

        backtrack(count + 1, depth + 1);

        if (req_idx != -1) required_used[req_idx] = false;
        current.pop_back();
        set_square(x, y, side, 0);

        if (DEBUG) cout << indent(depth) << "  - " << side << "x" << side
                        << " из (" << x+1 << "," << y+1 << ")\n";
    }
}

int main() {
    SetConsoleOutputCP(CP_UTF8);  
    SetConsoleCP(CP_UTF8);

    cin >> N >> M;

    required.clear();
    required_used.assign(M, false);
    for (int i = 0; i < M; i++) {
        int x, y, w;
        cin >> x >> y >> w;
        required.push_back({{x - 1, y - 1}, w});
    }

    if (DEBUG) {
        cout << "N=" << N << " M=" << M << "\n";
        for (int i = 0; i < M; i++)
            cout << "  обяз #" << i << ": (" << required[i].first.first+1
                 << "," << required[i].first.second+1
                 << ") W=" << required[i].second << "\n";
    }

    best_count = N * N + 1;
    empty_area = N * N;
    best_solution.clear();
    current.clear();

    // проверка обязательных
    bool valid = true;
    for (int i = 0; i < M; i++) {
        int rx = required[i].first.first;
        int ry = required[i].first.second;
        int rw = required[i].second;
        if (rw < 1 || rw > N - 1 || rx < 0 || ry < 0 || rx + rw > N || ry + rw > N) {
            valid = false;
            break;
        }
    }
    if (valid) {
        for (int i = 0; i < M && valid; i++) {
            for (int j = i + 1; j < M; j++) {
                int ax = required[i].first.first, ay = required[i].first.second, aw = required[i].second;
                int bx = required[j].first.first, by = required[j].first.second, bw = required[j].second;
                if (!(ax + aw <= bx || bx + bw <= ax || ay + aw <= by || by + bw <= ay)) {
                    valid = false;
                    break;
                }
            }
        }
    }

    if (!valid) {
        if (DEBUG) cout << "обязательные некорректны — решения нет\n";
        cout << "No solution\n";
        return 0;
    }

    if (N % 2 == 0 && M == 0) {
        if (DEBUG) cout << "чётный N без обязательных — 4 квадрата\n";
        int half = N / 2;
        best_count = 4;
        best_solution.push_back({{0, 0}, half});
        best_solution.push_back({{0, half}, half});
        best_solution.push_back({{half, 0}, half});
        best_solution.push_back({{half, half}, half});
    } else {
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++)
                board[i][j] = 0;

        for (int first = N - 1; first >= 1; first--) {
            if (conflicts_with_required(0, 0, first)) continue;

            int req_idx = find_required_idx(0, 0, first);

            if (DEBUG) {
                cout << "\n=== first " << first << "x" << first << " в (1,1)";
                if (req_idx != -1) cout << " [обяз #" << req_idx << "]";
                cout << " ===\n";
            }

            set_square(0, 0, first, 1);
            current.push_back({{0, 0}, first});
            if (req_idx != -1) required_used[req_idx] = true;

            backtrack(1, 1);

            if (req_idx != -1) required_used[req_idx] = false;
            current.pop_back();
            set_square(0, 0, first, 0);
        }
    }

    if (DEBUG) cout << "\nлучшее: " << best_count << " квадратов\n";

    if (best_count > N * N) {
        cout << "No solution\n";
    } else {
        cout << best_count << "\n";
        for (auto &sq : best_solution) {
            cout << sq.first.first + 1 << " "
                 << sq.first.second + 1 << " "
                 << sq.second << "\n";
        }
    }

    return 0;
}
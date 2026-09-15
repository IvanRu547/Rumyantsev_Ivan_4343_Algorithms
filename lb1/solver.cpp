#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int N;
int board[20][20];
int empty_area;
int best_count;
vector<pair<pair<int,int>,int>> best_solution;
vector<pair<pair<int,int>,int>> current;

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

void backtrack(int count) {
    // стандартное отсечение: если уже не меньше рекорда, и поле не заполнено — выходим
    if (count >= best_count && empty_area > 0) return;

    // все клетки заполнены
    if (empty_area == 0) {
        if (count < best_count) {
            best_count = count;
            best_solution = current;
        }
        return;
    }

    int x, y;
    if (!find_empty(x, y)) return;

    int max_side = min(N - x, N - y);
    if (max_side > N - 1) max_side = N - 1;

    // нижняя оценка по площади (безопасная)
    int lb = (empty_area + max_side * max_side - 1) / (max_side * max_side);
    if (count + lb >= best_count) return;

    for (int side = max_side; side >= 1; side--) {
        if (!can_place(x, y, side)) continue;
        set_square(x, y, side, 1);
        current.push_back({{x, y}, side});
        backtrack(count + 1);
        current.pop_back();
        set_square(x, y, side, 0);
    }
}

int main() {
    cin >> N;

    best_count = N * N + 1;
    empty_area = N * N;
    best_solution.clear();
    current.clear();

    if (N % 2 == 0) {
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

        // первый квадрат всегда в (0,0), перебираем от N-1 до 1
        for (int first = N - 1; first >= 1; first--) {
            set_square(0, 0, first, 1);
            current.push_back({{0, 0}, first});
            backtrack(1);
            current.pop_back();
            set_square(0, 0, first, 0);
        }
    }

    cout << best_count << "\n";
    for (auto &sq : best_solution) {
        cout << sq.first.first + 1 << " "
             << sq.first.second + 1 << " "
             << sq.second << "\n";
    }

    return 0;
}
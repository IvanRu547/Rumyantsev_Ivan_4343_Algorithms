import tkinter as tk

class KMPApp:
    def __init__(self, root):
        self.root = root
        root.title("КМП")
        root.geometry("750x550")
        root.resizable(False, False)

        self.mode = tk.StringVar(value="search")
        self.steps = []
        self.pos = 0
        self.auto = False

        # режим
        f = tk.Frame(root); f.pack(fill="x", padx=10, pady=5)
        tk.Label(f, text="Режим:").pack(side="left")
        tk.Radiobutton(f, text="Поиск", variable=self.mode, value="search",
                       command=self.clear).pack(side="left")
        tk.Radiobutton(f, text="Сдвиг", variable=self.mode, value="shift",
                       command=self.clear).pack(side="left")

        # ввод
        f = tk.Frame(root); f.pack(fill="x", padx=10, pady=5)
        tk.Label(f, text="Шаблон:").grid(row=0, column=0, sticky="w")
        self.e1 = tk.Entry(f, width=60); self.e1.grid(row=0, column=1, padx=5)
        tk.Label(f, text="Текст:").grid(row=1, column=0, sticky="w")
        self.e2 = tk.Entry(f, width=60); self.e2.grid(row=1, column=1, padx=5)

        # кнопки
        f = tk.Frame(root); f.pack(fill="x", padx=10, pady=5)
        tk.Button(f, text="Старт", width=8, command=self.start).pack(side="left", padx=2)
        tk.Button(f, text="Шаг", width=8, command=self.step).pack(side="left", padx=2)
        tk.Button(f, text="Авто", width=8, command=self.run_auto).pack(side="left", padx=2)
        tk.Button(f, text="Сброс", width=8, command=self.clear).pack(side="left", padx=2)

        # вывод
        f = tk.Frame(root); f.pack(fill="both", padx=10, pady=5)
        self.out = tk.Text(f, font=("Consolas", 10), height=22, width=90)
        sb = tk.Scrollbar(f, command=self.out.yview)
        self.out.configure(yscrollcommand=sb.set)
        self.out.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def log(self, s):
        self.out.insert(tk.END, s + "\n")
        self.out.see(tk.END)

    def clear(self):
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)
        self.out.delete("1.0", tk.END)
        self.steps = []
        self.pos = 0
        self.auto = False

    def prefix(self, P, log):
        m = len(P)
        pi = [0] * m
        log.append(f"pi[0] = 0")
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and P[i] != P[j]:
                log.append(f"i={i}: {P[i]}!={P[j]}, j={j}->{pi[j-1]}")
                j = pi[j - 1]
            if P[i] == P[j]:
                j += 1
                log.append(f"i={i}: совпадение, j={j}")
            else:
                log.append(f"i={i}: нет совпадения")
            pi[i] = j
            log.append(f"pi = {pi}")
        return pi

    # ---------- поиск вхождений ----------
    def build_search(self, P, T):
        log = [f"Шаблон: {P}", f"Текст: {T}", "--- префикс-функция ---"]
        pi = self.prefix(P, log)
        log.append(f"pi = {pi}")
        log.append("--- поиск ---")
        m, n = len(P), len(T)
        j = 0
        found = []
        for i in range(n):
            while j > 0 and T[i] != P[j]:
                log.append(f"i={i}: {T[i]}!={P[j]}, j={j}->{pi[j-1]}")
                j = pi[j - 1]
            if T[i] == P[j]:
                j += 1
            if j == m:
                pos = i - m + 1
                found.append(pos)
                log.append(f"найдено в позиции {pos}")
                j = pi[j - 1]
        log.append(f"Ответ: {','.join(map(str, found)) if found else -1}")
        return log

    # ---------- циклический сдвиг ----------
    def build_shift(self, A, B):
        if len(A) != len(B):
            return ["Разные длины", "Ответ: -1"]
        if not A:
            return ["Ответ: 0"]
        log = [f"A = {A}", f"B = {B}", f"A+A = {A+A}", "--- префикс-функция для B ---"]
        P = B
        pi = self.prefix(P, log)
        log.append(f"pi = {pi}")
        log.append("--- поиск ---")
        m, n = len(P), len(A + A)
        T = A + A
        j = 0
        for i in range(n):
            while j > 0 and T[i] != P[j]:
                j = pi[j - 1]
            if T[i] == P[j]:
                j += 1
            if j == m:
                pos = i - m + 1
                if pos < len(A):
                    log.append(f"найдено в позиции {pos}")
                    log.append(f"Ответ: {pos}")
                else:
                    log.append(f"найдено в позиции {pos} (за границей)")
                    log.append("Ответ: -1")
                return log
        log.append("Ответ: -1")
        return log

    def start(self):
        self.out.delete("1.0", tk.END)
        self.steps = []
        self.pos = 0
        self.auto = False
        P = self.e1.get().strip()
        T = self.e2.get().strip()
        if self.mode.get() == "search":
            if not P or not T:
                self.log("Заполни оба поля")
                return
            self.steps = self.build_search(P, T)
        else:
            self.steps = self.build_shift(P, T)
        self.log("Нажми «Шаг» или «Авто»")

    def step(self):
        if self.pos >= len(self.steps):
            return
        self.log(self.steps[self.pos])
        self.pos += 1

    def run_auto(self):
        self.auto = True
        self._tick()

    def _tick(self):
        if not self.auto or self.pos >= len(self.steps):
            self.auto = False
            return
        self.log(self.steps[self.pos])
        self.pos += 1
        self.root.after(300, self._tick)


if __name__ == "__main__":
    root = tk.Tk()
    KMPApp(root)
    root.mainloop()
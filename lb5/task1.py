import sys
from collections import deque

DEBUG = False  

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.children = {}       
        self.suffix_link = 0
        self.terminal_link = 0
        self.pattern_indices = []
        self.parent = 0
        self.parent_char = ''

def build_aho_corasick(patterns):
    trie = [Node(0)]
    for p_idx, p in enumerate(patterns):
        if not p:
            continue
        curr = 0
        for char in p:
            if char not in trie[curr].children:
                trie[curr].children[char] = len(trie)
                trie.append(Node(len(trie)))
                trie[-1].parent = curr
                trie[-1].parent_char = char
            curr = trie[curr].children[char]
        trie[curr].pattern_indices.append(p_idx)
    
    q = deque()
    for char, child in trie[0].children.items():
        trie[child].suffix_link = 0
        q.append(child)
        
    while q:
        curr = q.popleft()
        for char, child in trie[curr].children.items():
            q.append(child)
            temp = trie[curr].suffix_link
            while temp != 0 and char not in trie[temp].children:
                temp = trie[temp].suffix_link
            
            if char in trie[temp].children:
                trie[child].suffix_link = trie[temp].children[char]
            else:
                trie[child].suffix_link = 0
                
            sl = trie[child].suffix_link
            if trie[sl].pattern_indices:
                trie[child].terminal_link = sl
            else:
                trie[child].terminal_link = trie[sl].terminal_link
                
    return trie

def search_aho_corasick(text, trie):
    results = []
    curr = 0
    for i, char in enumerate(text):
        if DEBUG:
            print(f"Шаг {i}: символ '{char}', текущая вершина {curr}", end="")
            
        while curr != 0 and char not in trie[curr].children:
            if DEBUG:
                print(f" -> суф. ссылка в {trie[curr].suffix_link}", end="")
            curr = trie[curr].suffix_link
        
        if char in trie[curr].children:
            curr = trie[curr].children[char]
            if DEBUG:
                print(f" -> переход в {curr}", end="")
        else:
            curr = 0
            if DEBUG:
                print(" -> остаемся в 0", end="")
                
        matches = []
        temp = curr
        while True:
            if trie[temp].pattern_indices:
                matches.extend(trie[temp].pattern_indices)
            if temp == 0:
                break
            temp = trie[temp].terminal_link
            
        if matches:
            if DEBUG:
                print(f" | НАЙДЕНЫ ШАБЛОНЫ (индексы): {matches}")
            for p_idx in matches:
                results.append((i, p_idx))
        elif DEBUG:
            print()
            
    return results

def print_debug_info(trie, patterns, text):
    print("\n=== ПОСТРОЕНИЕ БОРА ===")
    for i, node in enumerate(trie):
        parent_info = f"родитель={node.parent}, символ='{node.parent_char}'" if i > 0 else "корень"
        patterns_info = f", шаблоны={node.pattern_indices}" if node.pattern_indices else ""
        print(f"Вершина {i}: {parent_info}{patterns_info}")
        
    print("\n=== ПОСТРОЕНИЕ АВТОМАТА (ссылки) ===")
    for i, node in enumerate(trie):
        print(f"Вершина {i}: суффиксная ссылка={node.suffix_link}, конечная ссылка={node.terminal_link}")
        
    print("\n=== ОПИСАНИЕ КАЖДОЙ ВЕРШИНЫ ===")
    for i, node in enumerate(trie):
        children_str = ", ".join([f"'{k}':{v}" for k, v in node.children.items()])
        print(f"Вершина {i}: переходы=[{children_str}], suff={node.suffix_link}, term={node.terminal_link}, patterns={node.pattern_indices}")
    print("\n=== ПРОЦЕСС ИСПОЛЬЗОВАНИЯ АВТОМАТА ===")

def solve_task1():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    

    lines = [line.strip() for line in input_data if line.strip()]
    if len(lines) < 2:
        return
        
    text = lines[0]
    n = int(lines[1])
    patterns = [line for line in lines[2:2+n]]
    
    trie = build_aho_corasick(patterns)
    
    if DEBUG:
        print_debug_info(trie, patterns, text)
        
    results = search_aho_corasick(text, trie)
    
    ans = []
    for end_idx, p_idx in results:
        start_idx = end_idx - len(patterns[p_idx]) + 1
        ans.append((start_idx + 1, p_idx + 1))
        
    ans.sort(key=lambda x: (x[0], x[1]))
    
    for start, p in ans:
        print(f"{start} {p}")

if __name__ == "__main__":
    solve_task1()
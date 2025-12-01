"""
Approximation Algorithm for TSP (Greedy Nearest Neighbor + 2-opt with random restarts)
John Henry Adams, Dylan Dao, Harry Williams
"""
import math
import random
import time
import sys


def greedy_tsp(dist, start=0):
    n = len(dist)
    visited = [False] * n
    current = start
    visited[current] = True
    path = [current]
    cost = 0.0

    for _ in range(n - 1):
        best = math.inf
        ties = []
        for v in range(n):
            if not visited[v]:
                d = dist[current][v]
                if d < best - 1e-12:
                    best = d
                    ties = [v]
                elif abs(d - best) <= 1e-12:
                    ties.append(v)
        nxt = random.choice(ties)
        visited[nxt] = True
        path.append(nxt)
        cost += best
        current = nxt

    cost += dist[current][start]
    path.append(start)
    return cost, path


def two_opt(dist, path):
    """In-place 2-opt on a cycle. Returns improved cycle path (last equals first)."""
    n = len(path) - 1
    route = path[:-1]
    improved = True

    while improved:
        improved = False
        for i in range(n - 1):
            a, b = route[i], route[(i + 1) % n]
            for j in range(i + 2, n if i > 0 else n - 1):
                c, d = route[j], route[(j + 1) % n]
                
                current_cost = dist[a][b] + dist[c][d]
                new_cost = dist[a][c] + dist[b][d]
                
                # If swapping improves, reverse segment
                if new_cost < current_cost - 1e-12:
                    route[i + 1:j + 1] = reversed(route[i + 1:j + 1])
                    improved = True
                    break
            if improved:
                break
    
    return route + [route[0]]


def solve_with_restarts(dist, time_limit=1.8, k_starts=20, log_series_path=None, seed=412):
    n = len(dist)
    start_time = time.time()
    
    best_cost = math.inf
    best_path = None
    
    while time.time() - start_time < time_limit:
        # Random starting node
        start_node = random.randint(0, n - 1)
        cost, path = greedy_tsp(dist, start_node)
        
        # Apply 2-opt local search
        improved_path = two_opt(dist, path)
        
        # Calculate improved cost
        improved_cost = sum(dist[improved_path[i]][improved_path[i+1]] 
                          for i in range(len(improved_path) - 1))
        
        if improved_cost < best_cost:
            best_cost = improved_cost
            best_path = improved_path
    
    return best_cost, best_path

def read_complete_graph(stdin):
    header = stdin.readline().strip()
    if not header:
        raise ValueError("Empty input")
    _, m = map(int, header.split())
    edges = []
    names = {}
    for _ in range(m):
        a, b, w = stdin.readline().split()
        edges.append((a, b, float(w)))
        if a not in names:
            names[a] = len(names)
        if b not in names:
            names[b] = len(names)

    n = len(names)
    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    
    for a, b, w in edges:
        i, j = names[a], names[b]
        dist[i][j] = dist[j][i] = w
    return dist, names


def main():
    TIME_LIMIT = 1.8
    K_STARTS = 20

    dist, names = read_complete_graph(sys.stdin)
    cost, path = solve_with_restarts(dist, time_limit=TIME_LIMIT, k_starts=K_STARTS)
    idx_to_name = {v: k for k, v in names.items()}

    print(f"{cost:.4f}")
    print(" ".join(idx_to_name[i] for i in path))

if __name__ == "__main__":
    main()

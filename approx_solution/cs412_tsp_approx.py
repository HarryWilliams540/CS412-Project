"""
Approximation Algorithm for TSP (Nearest Neighbor + 2-opt with random restarts)
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
                if dist[a][c] + dist[b][d] < dist[a][b] + dist[c][d] - 1e-12:
                    route[i + 1:j + 1] = reversed(route[i + 1:j + 1])
                    improved = True
                    break
            if improved:
                break
    return route + [route[0]]


def solve_with_restarts(dist, time_limit=1.8, k_starts=20, log_series_path=None, seed=412):
    n = len(dist)
    random.seed(seed)
    t0 = time.time()
    deadline = t0 + max(0.01, time_limit)
    best_cost = math.inf
    best_path = None

    starts = [0]
    if n > 1:
        # Sample without replacement; if k_starts > n fall back to full range
        extra = min(k_starts - 1, n - 1)
        starts += random.sample(range(1, n), extra)

    log = open(log_series_path, "w") if log_series_path else None
    if log:
        log.write("t_ms,run_idx,start_node,before_cost,after_cost,improve,improve_ratio,local_min,best_so_far,best_per_node\n")

    for run_idx, start in enumerate(starts):
        if time.time() >= deadline:
            break
        _, path = greedy_tsp(dist, start)
        before = sum(dist[path[i]][path[i+1]] for i in range(n))
        path = two_opt(dist, path)
        after = sum(dist[path[i]][path[i+1]] for i in range(n))
        improve = before - after
        improve_ratio = improve / before if before > 0 else 0.0
        local_min = int(after >= before - 1e-12)
        if after < best_cost - 1e-12:
            best_cost, best_path = after, path
        if log:
            t_ms = int((time.time() - t0) * 1000)
            log.write(f"{t_ms},{run_idx},{start},{before:.6f},{after:.6f},{improve:.6f},{improve_ratio:.6f},{local_min},{best_cost:.6f},{(best_cost/n):.6f}\n")

    if log:
        log.close()

    if best_path is None:
        best_cost, best_path = greedy_tsp(dist, 0)
        best_path = two_opt(dist, best_path)
        best_cost = sum(dist[best_path[i]][best_path[i+1]] for i in range(n))
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
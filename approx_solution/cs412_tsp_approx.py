"""
Approximation Algorithm for TSP (Greedy Nearest Neighbor + 2-opt with Anytime Restarts)
CS 412 Project
"""

import sys
import math
import time
import random

def read_complete_graph(stdin):
    """Reads a complete graph from stdin. Returns distance matrix and name map."""
    try:
        header = stdin.readline().split()
        if not header: return None, None
        n, m = int(header[0]), int(header[1])

        names = {}
        dist = [[0.0] * n for _ in range(n)]
        next_idx = 0

        for _ in range(m):
            parts = stdin.readline().split()
            u, v, w = parts[0], parts[1], float(parts[2])
            
            if u not in names:
                names[u] = next_idx
                next_idx += 1
            if v not in names:
                names[v] = next_idx
                next_idx += 1
            
            i, j = names[u], names[v]
            dist[i][j] = dist[j][i] = w
            
        return dist, names
    except ValueError:
        return None, None

def greedy_tsp(dist, start_node):
    """Constructs a greedy tour from start_node."""
    n = len(dist)
    visited = [False] * n
    path = [start_node]
    visited[start_node] = True
    cost = 0.0
    current = start_node

    for _ in range(n - 1):
        best_next = -1
        min_dist = math.inf
        
        for neighbor in range(n):
            if not visited[neighbor]:
                d = dist[current][neighbor]
                if d < min_dist:
                    min_dist = d
                    best_next = neighbor
                elif d == min_dist:
                    # Random tie-breaking
                    if random.random() < 0.5:
                        best_next = neighbor
        
        visited[best_next] = True
        path.append(best_next)
        cost += min_dist
        current = best_next

    cost += dist[current][start_node]
    path.append(start_node)
    return cost, path

def calculate_path_cost(dist, path):
    return sum(dist[path[i]][path[i+1]] for i in range(len(path)-1))

def two_opt(dist, path):
    """
    Performs 2-opt local search to improve the tour.
    Iterates until no improving swap is found (local minimum).
    """
    n = len(path) - 1 # path has n+1 nodes (start repeated)
    improved = True
    best_path = path[:]
    
    while improved:
        improved = False
        # Iterate over all possible segments to swap
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1: continue # Skip adjacent edges
                
                # Nodes involved in the swap
                u, v = best_path[i-1], best_path[i]
                x, y = best_path[j], best_path[j+1]
                
                # Check if swap reduces length
                current_dist = dist[u][v] + dist[x][y]
                new_dist = dist[u][x] + dist[v][y]
                
                if new_dist < current_dist:
                    # Perform the swap: reverse segment [i, j]
                    best_path[i:j+1] = best_path[i:j+1][::-1]
                    improved = True
                    
    return best_path

def solve_with_restarts(dist, time_limit=1.8, k_starts=20, log_series_path=None, seed=412):
    """
    Anytime algorithm: Runs Greedy + 2-Opt with random restarts.
    Stops when time_limit expires or k_starts is reached.
    """
    n = len(dist)
    random.seed(seed)
    start_time = time.time()
    deadline = start_time + time_limit

    best_cost = math.inf
    best_path = None

    log_file = open(log_series_path, "w") if log_series_path else None
    if log_file:
        log_file.write("t_ms,run_idx,start_node,greedy_cost,localsearch_cost,improve,best_so_far\n")

    start_nodes = [0]
    if n > 1:
        pool = list(range(1, n))
        count = min(k_starts - 1, len(pool))
        start_nodes += random.sample(pool, count)

    for run_idx, start_node in enumerate(start_nodes):
        if time.time() >= deadline:
            break

        g_cost, g_path = greedy_tsp(dist, start_node)

        ls_path = two_opt(dist, g_path)
        ls_cost = calculate_path_cost(dist, ls_path)

        if ls_cost < best_cost:
            best_cost = ls_cost
            best_path = ls_path

        # Log Data
        if log_file:
            t_ms = int((time.time() - start_time) * 1000)
            improve = g_cost - ls_cost
            log_file.write(f"{t_ms},{run_idx},{start_node},{g_cost:.4f},{ls_cost:.4f},{improve:.4f},{best_cost:.4f}\n")

    if log_file:
        log_file.close()

    # Fallback if loop didn't run
    if best_path is None:
        return greedy_tsp(dist, 0)

    return best_cost, best_path

def main():
    dist, names = read_complete_graph(sys.stdin)
    if dist is None:
        return

    cost, path = solve_with_restarts(dist, time_limit=1.9, k_starts=50)
    print(f"{cost:.4f}")
    
    idx_to_name = {v: k for k, v in names.items()}
    path_names = [idx_to_name[i] for i in path]
    print(" ".join(path_names))

if __name__ == "__main__":
    main()
"""
Approximation Algorithm for TSP (Greedy Nearest Neighbor + 2-opt with random restarts)
John Henry Adams, Dylan Dao, Harry Williams
"""
import math
import random
import time


def greedy_tsp(dist, start=0):
    n = len(dist)

    current = start
    visited = [False] * n
    visited[start] = True
    path = [start]
    total_cost = 0.0

    for _ in range(n - 1):
        best_dist = math.inf
        candidates = []

        for next_node in range(n):
            if not visited[next_node]:
                d = dist[current][next_node]
                if d < best_dist - 1e-12:
                    best_dist = d
                    candidates = [next_node]
                elif abs(d - best_dist) <= 1e-12:
                    candidates.append(next_node)

        next_node = random.choice(candidates)
        visited[next_node] = True
        path.append(next_node)
        total_cost += best_dist
        current = next_node

    total_cost += dist[current][start]
    path.append(start)

    return total_cost, path


def two_opt(dist, path):
    """Apply 2-opt local search to improve tour."""
    n = len(path) - 1
    route = path[:-1]
    improved = True
    
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Calculate current edge costs
                a, b = route[i], route[(i + 1) % n]
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


# Run greedy + 2-opt with multiple random starts.
def solve_with_restarts(dist, time_limit=1.8):
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


def main():
    _, m = map(int, input().split())

    edges = []
    names = {}
    for _ in range(m):
        a, b, w = input().split()
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

    cost, path = solve_with_restarts(dist)
    idx_to_name = {v: k for k, v in names.items()}
    print(f"{cost:.4f}")
    print(" ".join(idx_to_name[i] for i in path))


if __name__ == "__main__":
    main()
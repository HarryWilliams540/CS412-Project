"""
starts with complete graph
Hamiltonian cycle
John Henry Adams, Dylan Dao, Harry Williams

Example input:
3 3
a b 3.0
b c 4.2
a c 5.4

Example output:
5.4
a b c
12.6000
a b c a
"""

import itertools
import math


def brute_force_tsp(dist):
    n = len(dist)
    if n == 0:
        return 0.0, ( )
    if n == 1:
        return 0.0, (0, 0)
    
    best_cost = None
    best_path = None

    for perm in itertools.permutations(range(1, n)):
        tour = (0,) + perm + (0,)
        cost = sum(dist[tour[i]][tour[i+1]] for i in range(n))

        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_path = tour

    return best_cost, best_path


def main():
    _, m = map(int, input().split())

    edges = []
    names = {}
    for _ in range(m):
        a, b, w = input().split()
        edges.append((a, b, float(w)))
        names[a] = names.get(a, len(names))
        names[b] = names.get(b, len(names))

    size = len(names)
    dist = [[math.inf] * size for _ in range(size)]
    for i in range(size):
        dist[i][i] = 0.0
    
    for a, b, w in edges:
        i, j = names[a], names[b]
        dist[i][j] = dist[j][i] = w

    cost, path = brute_force_tsp(dist)
    idx_to_name = {v: k for k, v in names.items()}
    print(f"{cost:.4f}")
    print(" ".join(idx_to_name[i] for i in path))


if __name__ == "__main__":
    main()

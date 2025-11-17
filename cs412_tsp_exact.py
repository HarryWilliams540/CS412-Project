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
    best_cost = float("inf")
    best_path = None

    for perm in itertools.permutations(range(1, n)):
        tour = (0,) + perm + (0,)
        cost = sum(dist[tour[i]][tour[i+1]] for i in range(n))

        if cost < best_cost:
            best_cost = cost
            best_path = tour

    return best_cost, best_path


def main():
    n, m = map(int, input().split())

    name_to_idx = {}
    idx_to_name = []

    idx = 0

    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0

    for _ in range(m):
        a, b, w = input().split()
        w = float(w)

        # Assign indices for new names
        if a not in name_to_idx:
            name_to_idx[a] = idx
            idx_to_name.append(a)   
            idx += 1
        if b not in name_to_idx:
            name_to_idx[b] = idx
            idx_to_name.append(b)
            idx += 1

        i = name_to_idx[a]
        j = name_to_idx[b]

        dist[i][j] = w
        dist[j][i] = w

    best_cost, best_path = brute_force_tsp(dist)

    print(f"{best_cost:.4f}")
    named_path = [idx_to_name[i] for i in best_path]
    print(" ".join(named_path))


if __name__ == "__main__":
    main()

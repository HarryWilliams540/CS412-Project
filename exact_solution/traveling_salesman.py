# starts with complete graph
# Hamiltonian cycle
# John Henry Adams, Dylan Dao, Harry Williams
"""Number of cities: 4
City 1: 0 10 15 20
City 2: 0 0 35 25
City 3: 15 35 0 30
City 4: 20 25 30 0
"""
import itertools


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
    n = int(input("Number of cities: "))
    dist = []
    for i in range(1, n + 1):
        row = list(map(int, input(f"City {i}: ").split()))
        dist.append(row)

    print(brute_force_tsp(dist))


if __name__ == "__main__":
    main()

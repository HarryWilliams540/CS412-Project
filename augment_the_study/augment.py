"""
The goal of this augmentation is to find
the lower bound of our approximation.
The value of our approximation will never
be lower than the lower bound. We will be
calculating using the 1-tree bound method which
uses a minimum spanning tree.
"""
import math
import heapq


def read_graph():
    # First line: n m
    n, m = input().split()
    n, m = int(n), int(m)

    # Create n x n matrix with infinities
    D = [[math.inf]*n for _ in range(n)]

    # Map city labels to indices
    label_to_idx = {}
    next_idx = 0

    for _ in range(m):
        a, b, w = input().split()
        w = float(w)

        # assign indices if needed
        if a not in label_to_idx:
            label_to_idx[a] = next_idx
            next_idx += 1
        if b not in label_to_idx:
            label_to_idx[b] = next_idx
            next_idx += 1

        i = label_to_idx[a]
        j = label_to_idx[b]

        # undirected complete graph edge
        D[i][j] = w
        D[j][i] = w

    return n, D


def prim_mst_cost(D, excluded=None):
    """
    Compute MST of all nodes except 'excluded'
    """
    n = len(D)

    visited = [False] * n
    if excluded is not None:
        visited[excluded] = True  # exclude this node

    # pick any start node ≠ excluded
    start = 0 if excluded != 0 else 1

    visited[start] = True
    pq = []

    # push edges from start
    for v in range(n):
        if not visited[v]:
            heapq.heappush(pq, (D[start][v], v))

    total = 0.0

    while pq:
        w, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        total += w

        for v in range(n):
            if not visited[v]:
                heapq.heappush(pq, (D[u][v], v))

    return total


def one_tree_cost(D, root):
    """
    Compute 1-tree cost:
    MST on V - {root} + two smallest edges incident to root
    """

    n = len(D)
    # MST on all vertices except root
    mst_cost = prim_mst_cost(D, excluded=root)

    # find two smallest edges from root
    edges = sorted(D[root][v] for v in range(n) if v != root)

    return mst_cost + edges[0] + edges[1]


def one_tree_lower_bound(D):
    """
    Try all roots and take the maximum 1-tree cost.
    """
    n = len(D)
    best = -1
    for r in range(n):
        c = one_tree_cost(D, r)
        best = max(best, c)
    return best


# -------- main program --------
if __name__ == "__main__":
    n, D = read_graph()
    lb = one_tree_lower_bound(D)
    print("1-tree lower bound:", lb)

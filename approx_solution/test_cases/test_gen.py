import math
import os
import random
from pathlib import Path

def euclid(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def gen_points(n, idx, variant):
    # Reproducible per (bucket index, variant)
    random.seed(412_000 + idx * 1000 + variant)
    pts = []
    # Use your previous regimes but diversify by variant
    if variant == 0:
        # Uniform square
        for _ in range(n):
            pts.append((random.random(), random.random()))
    elif variant == 1:
        # 4–6 clusters
        k = 4 + (idx % 3)  # 4..6 clusters
        centers = [(random.random(), random.random()) for _ in range(k)]
        sigma = 0.03 + 0.005 * (idx % 5)
        for i in range(n):
            cx, cy = centers[i % k]
            pts.append((
                max(0.0, min(1.0, random.gauss(cx, sigma))),
                max(0.0, min(1.0, random.gauss(cy, sigma))),
            ))
    elif variant == 2:
        # Clusters + outliers ring
        k = 5
        centers = [(random.random(), random.random()) for _ in range(k)]
        sigma = 0.025
        outliers = max(10, n // 40)
        for i in range(n - outliers):
            cx, cy = centers[i % k]
            pts.append((
                max(0.0, min(1.0, random.gauss(cx, sigma))),
                max(0.0, min(1.0, random.gauss(cy, sigma))),
            ))
        R = 3.0 + 0.2 * (idx % 4)
        for j in range(outliers):
            ang = 2.0 * math.pi * j / outliers
            pts.append((R * math.cos(ang), R * math.sin(ang)))
    elif variant == 3:
        # Noisy circle
        R = 1.0
        jitter = 0.02 + 0.005 * (idx % 4)
        for i in range(n):
            ang = 2.0 * math.pi * i / n
            r = R + random.uniform(-jitter, jitter)
            pts.append((r * math.cos(ang), r * math.sin(ang)))
    else:
        # Two dense clusters + bridges
        A = [(random.gauss(0.2, 0.03), random.gauss(0.5, 0.03)) for _ in range(n // 2)]
        B = [(random.gauss(0.8, 0.03), random.gauss(0.5, 0.03)) for _ in range(n - len(A))]
        pts = A + B
        # Add a few bridge points along the middle to create greedy traps
        bridges = min(10, n // 100)
        for b in range(bridges):
            t = (b + 1) / (bridges + 1)
            pts[b] = (0.2 + 0.6 * t + random.uniform(-0.01, 0.01),
                      0.5 + random.uniform(-0.02, 0.02))
    return pts

def write_complete_graph(path, pts, names):
    n = len(pts)
    m = n * (n - 1) // 2
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{n} {m}\n")
        for i in range(n):
            for j in range(i + 1, n):
                w = euclid(pts[i], pts[j])
                if w < 1e-9:
                    w = 1e-9
                f.write(f"{names[i]} {names[j]} {w:.4f}\n")

def main():
    out_dir = Path(__file__).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Buckets: n = 100, 200, ..., 2000 (inclusive); 5 variants per n
    for n in range(100, 2001, 100):
        for variant in range(5):  # 0..4
            idx = (n // 100)  # bucket index 1..20
            names = [f"v{i+1}" for i in range(n)]
            pts = gen_points(n, idx, variant)
            fname = out_dir / f"auto_n{n:04d}_v{variant:01d}.txt"
            write_complete_graph(fname, pts, names)
    print("Generated", len(list(out_dir.glob("auto_n*.txt"))), "cases in", out_dir)

if __name__ == "__main__":
    main()
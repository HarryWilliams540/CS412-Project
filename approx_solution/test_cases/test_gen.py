# ...existing code...
import math
import os
import random
from pathlib import Path

def euclid(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def gen_points(n, idx):
    random.seed(412 + idx)  # reproducible but varied per case
    pts = []
    if idx <= 30:
        # Uniform square
        for _ in range(n):
            pts.append((random.random(), random.random()))
    elif idx <= 60:
        # 3–5 clusters with small noise
        k = 3 + (idx // 10)
        centers = [(random.random(), random.random()) for _ in range(k)]
        sigma = 0.03 + 0.002 * (idx - 30)
        for i in range(n):
            cx, cy = centers[i % k]
            pts.append((
                max(0.0, min(1.0, random.gauss(cx, sigma))),
                max(0.0, min(1.0, random.gauss(cy, sigma))),
            ))
    elif idx <= 80:
        # Clusters + a few far outliers to create greedy traps
        k = 4
        centers = [(random.random(), random.random()) for _ in range(k)]
        sigma = 0.02 + 0.002 * (idx - 60)
        outliers = max(2, n // 12)
        for i in range(n - outliers):
            cx, cy = centers[i % k]
            pts.append((
                max(0.0, min(1.0, random.gauss(cx, sigma))),
                max(0.0, min(1.0, random.gauss(cy, sigma))),
            ))
        # Place outliers in a ring far away (scaled shell)
        R = 3.0
        for j in range(outliers):
            ang = 2.0 * math.pi * j / outliers
            pts.append((R * math.cos(ang), R * math.sin(ang)))
    else:
        # Noisy circle/ring (near-equal neighbor distances → 2-opt gets interesting)
        R = 1.0
        jitter = 0.02 + 0.0005 * (idx - 80)
        for i in range(n):
            ang = 2.0 * math.pi * i / n
            r = R + random.uniform(-jitter, jitter)
            pts.append((r * math.cos(ang), r * math.sin(ang)))
    return pts

def write_complete_graph(path, pts, names):
    n = len(pts)
    m = n * (n - 1) // 2
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{n} {m}\n")
        for i in range(n):
            for j in range(i + 1, n):
                w = euclid(pts[i], pts[j])
                if w < 1e-9:  # avoid zero weights
                    w = 1e-9
                f.write(f"{names[i]} {names[j]} {w:.4f}\n")

def main():
    out_dir = Path(__file__).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate 100 cases with n = 5..104
    for idx in range(1, 101):
        n = 4 + idx  # 5..104
        names = [f"v{i+1}" for i in range(n)]
        pts = gen_points(n, idx)
        fname = out_dir / f"auto_{idx:03d}_n{n}.txt"
        write_complete_graph(fname, pts, names)
    print("Generated 100 cases in", out_dir)

if __name__ == "__main__":
    main()
# ...existing code...
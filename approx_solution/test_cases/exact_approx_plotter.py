import subprocess, pathlib, csv, math

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPROX = ROOT / "cs412_tsp_approx.py"
EXACT = ROOT.parent / "exact_solution" / "cs412_tsp_exact.py"
OUT = pathlib.Path(__file__).parent / "exact_vs_approx.csv"

def run(prog, path):
    out = subprocess.check_output(["python3", str(prog)], stdin=open(path, "r"), text=True).strip().splitlines()
    return float(out[0])

rows=[]
for f in sorted(pathlib.Path(__file__).parent.glob("auto_n0100_v*.txt")):
    approx = run(APPROX, f)
    exact = run(EXACT, f)
    gap = (approx - exact)/exact
    rows.append((f.name, exact, approx, gap))

with open(OUT, "w", newline="") as w:
    cw = csv.writer(w)
    cw.writerow(["input","exact_cost","approx_cost","gap_ratio"])
    cw.writerows(rows)

print("Wrote", OUT)
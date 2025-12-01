import csv, pathlib, statistics, math
import matplotlib.pyplot as plt

TS = pathlib.Path(__file__).parent / "time_series.csv"

def load():
    rows = []
    with open(TS, newline="") as f:
        r = csv.DictReader(f)
        header = r.fieldnames or []
        legacy = "improve" not in header  # detect old CSV without new columns
        for row in r:
            # Basic casts always present
            row["t_ms"] = int(row["t_ms"]) if row.get("t_ms") else 0
            row["run_idx"] = int(row.get("run_idx", 0))
            # Required numeric fields that might exist
            for k in ("before_cost", "after_cost", "best_so_far"):
                if k in row and row[k]:
                    row[k] = float(row[k])
                else:
                    row[k] = float('nan')
            # If legacy, compute improve/improve_ratio/best_per_node defensively
            if legacy:
                bc = row.get("before_cost", float('nan'))
                ac = row.get("after_cost", float('nan'))
                if not math.isnan(bc) and not math.isnan(ac):
                    improve = bc - ac
                    ratio = improve / bc if bc > 0 else 0.0
                else:
                    improve = float('nan')
                    ratio = float('nan')
                row["improve"] = improve
                row["improve_ratio"] = ratio
                # best_per_node: use best_so_far if present else after_cost
                base = row["best_so_far"] if not math.isnan(row["best_so_far"]) else row["after_cost"]
                # Attempt to infer n from filename pattern (auto_nXXXX_); else leave NaN
                if row.get("input"):
                    n = _infer_n(row["input"])
                    row["best_per_node"] = base / n if (n and base and not math.isnan(base)) else float('nan')
                else:
                    row["best_per_node"] = float('nan')
            else:
                # New format: cast declared fields
                for k in ("improve", "improve_ratio", "best_per_node"):
                    if k in row and row[k]:
                        row[k] = float(row[k])
                    else:
                        row[k] = float('nan')
            rows.append(row)
    return rows

def _infer_n(name: str):
    # Expect pattern auto_nXXXX_vY.txt
    try:
        if "n" in name:
            # split on '_' then find the token starting with 'n'
            for part in name.split('_'):
                if part.startswith('n') and part[1:].isdigit():
                    return int(part[1:])
    except Exception:
        return None
    return None

def group(rows):
    g={}
    for r in rows:
        g.setdefault(r["input"],[]).append(r)
    for k in g: g[k].sort(key=lambda x:x["t_ms"])
    return g

def plot_convergence_norm(g):
    plt.figure(figsize=(6,4))
    for name, seq in g.items():
        if len(seq)<3: continue
        t=[r["t_ms"]/1000.0 for r in seq]
        y=[r["best_per_node"] for r in seq]
        plt.plot(t,y,label=name)
    plt.xlabel("Time (s)")
    plt.ylabel("Best cost per node")
    plt.title("Normalized Convergence")
    plt.legend(fontsize="x-small")
    plt.tight_layout()
    plt.savefig("conv_normalized.png",dpi=150)

def plot_improvement_decay(g):
    plt.figure(figsize=(6,4))
    for name, seq in g.items():
        if len(seq)<5: continue
        plt.scatter([r["run_idx"] for r in seq],
                    [r["improve_ratio"] for r in seq],
                    s=14, alpha=0.5, label=name)
    plt.xlabel("Restart index")
    plt.ylabel("Improvement ratio")
    plt.title("Improvement Ratio per Restart")
    plt.legend(fontsize="x-small")
    plt.tight_layout()
    plt.savefig("improve_ratio.png",dpi=150)

def plot_variance(g):
    labels=[]; data=[]
    for name, seq in g.items():
        if len(seq)<5: continue
        labels.append(name)
        data.append([r["after_cost"] for r in seq])
    if not data: return
    plt.figure(figsize=(6,4))
    plt.boxplot(data, labels=labels, showfliers=False)
    plt.ylabel("Post 2-opt cost (raw)")
    plt.title("Variance Across Restarts (Raw Scale)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig("variance_raw.png",dpi=150)

def plot_improvement_cumulative(g):
    plt.figure(figsize=(6,4))
    for name, seq in g.items():
        if len(seq)<3: continue
        seq_sorted=sorted(seq,key=lambda r:r["run_idx"])
        cum=[]
        total=0.0
        for r in seq_sorted:
            total+=r["improve"]
            cum.append(total)
        plt.plot([r["run_idx"] for r in seq_sorted], cum, label=name)
    plt.xlabel("Restart index")
    plt.ylabel("Cumulative absolute improvement")
    plt.title("Cumulative Improvement Growth")
    plt.legend(fontsize="x-small")
    plt.tight_layout()
    plt.savefig("cumulative_improvement.png",dpi=150)

def main():
    rows=load()
    g=group(rows)
    plot_convergence_norm(g)
    plot_improvement_decay(g)
    plot_variance(g)
    plot_improvement_cumulative(g)
    print("Generated normalized plots.")

if __name__=="__main__":
    main()
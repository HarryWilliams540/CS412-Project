#!/bin/bash
set -euo pipefail

# Resolve Python interpreter
if command -v python3 >/dev/null 2>&1; then PY=(python3)
elif command -v python >/dev/null 2>&1; then PY=(python)
elif command -v py >/dev/null 2>&1; then PY=(py -3)
else
  echo "Python interpreter not found." >&2
  exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
APP="$ROOT/cs412_tsp_approx.py"

shopt -s nullglob
FILES=("$DIR"/auto_n*.txt)
if [ ${#FILES[@]} -eq 0 ]; then
  echo "No auto_n*.txt files found under $DIR" >&2
  exit 1
fi

OUT="$DIR/wallclock_results.csv"
echo "n,runtime_ms,best_cost,input" > "$OUT"

for file in "${FILES[@]}"; do
  echo "Running $(basename "$file")..."
  start_time=$(date +%s%3N)
  output="$("${PY[@]}" "$APP" < "$file")"
  end_time=$(date +%s%3N)
  ms=$((end_time - start_time))
  n=$(head -n1 "$file" | awk '{print $1}')
  best_cost=$(echo "$output" | head -n1)
  echo "$n,$ms,$best_cost,$(basename "$file")" >> "$OUT"
done

echo "Results written to $OUT"
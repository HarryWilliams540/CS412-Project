#!/bin/bash
set -euo pipefail
if command -v python3 >/dev/null 2>&1; then PY=(python3)
elif command -v python >/dev/null 2>&1; then PY=(python)
elif command -v py >/dev/null 2>&1; then PY=(py -3)
else echo "Python not found"; exit 1; fi

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
APP="$ROOT/cs412_tsp_approx.py"

FILES=(
  "$DIR/auto_n0100_v0.txt"
  "$DIR/auto_n0500_v2.txt"
  "$DIR/auto_n1000_v4.txt"
  "$DIR/auto_n2000_v1.txt"
)
for f in "${FILES[@]}"; do
  [ -f "$f" ] || { echo "Missing $f"; exit 1; }
  echo "Running $(basename "$f")..."
  start=$(date +%s%3N)
  "${PY[@]}" "$APP" --time-limit 1.0 --k 30 < "$f"
  end=$(date +%s%3N)
  echo "Completed in $((end - start)) ms"
  echo "--------------------------------"
done
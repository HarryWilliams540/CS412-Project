#!/bin/bash
set -euo pipefail

# Python resolver
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

# Hand pick a small variety plus the nonoptimal case
FILES=(
  "$DIR/auto_001_n5.txt"
  "$DIR/auto_005_n9.txt"
  "$DIR/auto_010_n14.txt"
  "$DIR/auto_020_n24.txt"
  "$DIR/nonoptimal_example.txt"
)

for f in "${FILES[@]}"; do
  [ -f "$f" ] || { echo "Missing test case: $f" >&2; exit 1; }
  echo "Running $(basename "$f")"
  start=$(date +%s%3N)
  "${PY[@]}" "$APP" < "$f"
  end=$(date +%s%3N)
  echo "Elapsed $((end-start)) ms"
  echo "---------------------"
done
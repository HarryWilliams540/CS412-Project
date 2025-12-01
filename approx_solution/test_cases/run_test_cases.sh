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

# Paths
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
APP="$ROOT/cs412_tsp_approx.py"

CASES=(
  "$DIR/auto_n0100_v0.txt"
  "$DIR/auto_n0500_v2.txt"
  "$DIR/auto_n1000_v4.txt"
  "$DIR/nonoptimal_example.txt"
)

echo "Running approximation on selected test cases..."
for f in "${CASES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "Skipping missing case: $(basename "$f")"
    continue
  fi
  echo "Case: $(basename "$f")"
  "${PY[@]}" "$APP" < "$f"
  echo "----------------------------------------"
done
#!/bin/bash
set -euo pipefail

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
CASE="$DIR/nonoptimal_example.txt"

[ -f "$CASE" ] || { echo "Missing $CASE" >&2; exit 1; }

echo "Running nonoptimal_example.txt"
"${PY[@]}" "$APP" < "$CASE"